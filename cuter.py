import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import hashlib
from pathlib import Path
import threading


class FileSplitterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File Splitter - 文件分割工具")
        self.root.geometry("800x650")

        icon_file = 'logo.ico'
        if os.path.exists(icon_file):
            try:
                self.root.iconbitmap(icon_file)
            except:
                pass

        self.mode = tk.StringVar(value="split")
        self.chunk_size = tk.DoubleVar(value=24.0)
        self.file_path = tk.StringVar()
        self.output_dir = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        mode_frame = ttk.LabelFrame(main_frame, text="操作模式", padding="10")
        mode_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Radiobutton(mode_frame, text="分割文件", variable=self.mode,
                        value="split", command=self.on_mode_change).grid(row=0, column=0, padx=20)
        ttk.Radiobutton(mode_frame, text="合并文件", variable=self.mode,
                        value="merge", command=self.on_mode_change).grid(row=0, column=1, padx=20)

        file_frame = ttk.LabelFrame(main_frame, text="文件选择", padding="10")
        file_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Entry(file_frame, textvariable=self.file_path, width=60).grid(
            row=0, column=0, sticky=(tk.W, tk.E), padx=5)
        file_frame.columnconfigure(0, weight=1)

        ttk.Button(file_frame, text="浏览...", command=self.browse_file).grid(
            row=0, column=1, padx=5)

        self.split_frame = ttk.LabelFrame(main_frame, text="分割设置", padding="10")
        self.split_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(self.split_frame, text="分块大小 (MB):").grid(row=0, column=0, sticky=tk.W)
        ttk.Spinbox(self.split_frame, from_=1, to=1000, textvariable=self.chunk_size,
                    width=10).grid(row=0, column=1, sticky=tk.W, padx=5)

        self.merge_frame = ttk.LabelFrame(main_frame, text="合并设置", padding="10")

        ttk.Label(self.merge_frame, text="输出目录:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(self.merge_frame, textvariable=self.output_dir, width=50).grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(self.merge_frame, text="浏览...", command=self.browse_output).grid(
            row=0, column=2, padx=5)

        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.action_button = ttk.Button(action_frame, text="开始分割",
                                        command=self.start_operation, width=20)
        self.action_button.grid(row=0, column=0, padx=10)

        ttk.Button(action_frame, text="打开目录", command=self.open_directory,
                   width=15).grid(row=0, column=1, padx=10)

        log_frame = ttk.LabelFrame(main_frame, text="日志输出", padding="10")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        main_frame.rowconfigure(4, weight=1)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=90,
                                                  font=("Consolas", 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        self.status_label = ttk.Label(status_frame, text="就绪", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X)

        self.progress = ttk.Progressbar(status_frame, mode='indeterminate', length=750)
        self.progress.pack(fill=tk.X, pady=5)

        self.on_mode_change()

    def on_mode_change(self):
        if self.mode.get() == "split":
            self.split_frame.grid()
            self.merge_frame.grid_remove()
            self.action_button.config(text="开始分割")
        else:
            self.split_frame.grid_remove()
            self.merge_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
            self.action_button.config(text="开始合并")

    def browse_file(self):
        if self.mode.get() == "split":
            filename = filedialog.askopenfilename(title="选择要分割的文件")
        else:
            directory = filedialog.askdirectory(title="选择包含分块文件的文件夹")
            if directory:
                self.file_path.set(directory)
                self.log(f"已选择目录：{directory}")
                return
            return
        
        if filename:
            self.file_path.set(filename)
            self.log(f"已选择：{filename}")

    def browse_output(self):
        directory = filedialog.askdirectory(title="选择输出目录")
        if directory:
            self.output_dir.set(directory)
            self.log(f"输出目录：{directory}")

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def start_operation(self):
        if not self.file_path.get():
            messagebox.showerror("错误", "请先选择文件！")
            return

        self.progress.start()

        thread = threading.Thread(target=self.run_operation, daemon=True)
        thread.start()

    def run_operation(self):
        try:
            if self.mode.get() == "split":
                self.split_file_gui()
            else:
                self.merge_file_gui()
        except Exception as e:
            self.log(f"错误：{e}")
            self.update_status("操作失败")
        finally:
            self.progress.stop()

    def split_file_gui(self):
        file_path = self.file_path.get()
        chunk_size_mb = self.chunk_size.get()

        if not os.path.exists(file_path):
            self.log(f"错误：文件不存在 - {file_path}")
            self.update_status("文件不存在")
            return

        try:
            file_size = os.path.getsize(file_path)
            chunk_size = int(chunk_size_mb) * 1024 * 1024

            file_name = os.path.basename(file_path)
            file_dir = os.path.dirname(file_path) or '.'
            
            output_folder = os.path.join(file_dir, f"{file_name}_parts")
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            total_chunks = (file_size + chunk_size - 1) // chunk_size

            self.log("=" * 60)
            self.log(f"文件：{file_name}")
            self.log(f"大小：{file_size / (1024 * 1024):.2f} MB")
            self.log(f"分块大小：{int(chunk_size_mb)} MB ({chunk_size:,} 字节)")
            self.log(f"预计分块数：{total_chunks}")
            self.log(f"输出目录：{os.path.basename(output_folder)}")
            self.log("-" * 60)

            with open(file_path, 'rb') as f:
                chunk_num = 1
                while True:
                    chunk_data = f.read(chunk_size)
                    if not chunk_data:
                        break

                    chunk_file_name = f"{file_name}_{chunk_num}"
                    chunk_file_path = os.path.join(output_folder, chunk_file_name)

                    with open(chunk_file_path, 'wb') as chunk_file:
                        chunk_file.write(chunk_data)

                    actual_size = len(chunk_data)
                    self.log(f"[{chunk_num:03d}] {chunk_file_name} - {actual_size:,} 字节 ({actual_size / (1024 * 1024):.2f} MB)")

                    chunk_num += 1

            info_file_path = os.path.join(output_folder, f"{file_name}.splitinfo")
            
            file_hash = hashlib.md5()
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    file_hash.update(chunk)
            
            with open(info_file_path, 'w', encoding='utf-8') as info_file:
                info_file.write(f"original_name={file_name}\n")
                info_file.write(f"total_size={file_size}\n")
                info_file.write(f"chunk_size={chunk_size}\n")
                info_file.write(f"total_chunks={total_chunks}\n")
                info_file.write(f"md5_hash={file_hash.hexdigest()}\n")

            self.log("-" * 60)
            self.log(f"✓ 分割完成！共 {total_chunks} 个文件")
            self.log(f"信息文件：{os.path.basename(info_file_path)}")
            self.log(f"所有文件已保存到：{os.path.basename(output_folder)}")
            self.update_status("分割成功")

            messagebox.showinfo("成功", f"文件分割完成！\n共 {total_chunks} 个分块\n已保存到 {os.path.basename(output_folder)} 文件夹")

        except Exception as e:
            self.log(f"错误：{e}")
            import traceback
            self.log(traceback.format_exc())
            self.update_status("分割失败")

    def merge_file_gui(self):
        selected_path = self.file_path.get()
        output_dir = self.output_dir.get() or None

        try:
            if os.path.isdir(selected_path):
                file_dir = selected_path
            else:
                file_dir = os.path.dirname(selected_path) or '.'
            
            self.log("=" * 60)
            self.log(f"扫描目录：{file_dir}")
            
            original_name = None
            total_chunks = 0
            expected_md5 = None
            chunk_files = []
            
            info_files = [f for f in os.listdir(file_dir) if f.endswith('.splitinfo')]
            
            if info_files:
                self.log(f"找到信息文件：{info_files[0]}")
                info_file_path = os.path.join(file_dir, info_files[0])
                
                with open(info_file_path, 'r', encoding='utf-8') as info_file:
                    for line in info_file:
                        line = line.strip()
                        if '=' in line:
                            key, value = line.split('=', 1)
                            if key == 'original_name':
                                original_name = value
                            elif key == 'total_chunks':
                                total_chunks = int(value)
                            elif key == 'md5_hash':
                                expected_md5 = value
                
                if original_name and total_chunks > 0:
                    for i in range(1, total_chunks + 1):
                        chunk_path = os.path.join(file_dir, f"{original_name}_{i}")
                        if os.path.exists(chunk_path):
                            chunk_files.append(chunk_path)
                            self.log(f"找到分块：{os.path.basename(chunk_path)}")
                        else:
                            self.log(f"错误：缺少分块文件 - {os.path.basename(chunk_path)}")
                            self.update_status("缺少分块文件")
                            return
                    
                    self.log(f"通过信息文件识别：{original_name} ({total_chunks} 个分块)")
            
            if not chunk_files:
                self.log("未找到信息文件，尝试自动识别分块文件...")
                
                all_files = os.listdir(file_dir)
                potential_bases = set()
                
                for f in all_files:
                    if '_' in f:
                        parts = f.rsplit('_', 1)
                        if len(parts) == 2 and parts[1].isdigit():
                            potential_bases.add(parts[0])
                
                best_base = None
                max_chunks = 0
                
                for base in potential_bases:
                    counter = 1
                    while True:
                        chunk_path = os.path.join(file_dir, f"{base}_{counter}")
                        if os.path.exists(chunk_path):
                            counter += 1
                        else:
                            break
                    
                    if counter - 1 > max_chunks:
                        max_chunks = counter - 1
                        best_base = base
                
                if best_base and max_chunks > 0:
                    original_name = best_base
                    total_chunks = max_chunks
                    
                    for i in range(1, total_chunks + 1):
                        chunk_path = os.path.join(file_dir, f"{original_name}_{i}")
                        if os.path.exists(chunk_path):
                            chunk_files.append(chunk_path)
                            self.log(f"找到分块：{os.path.basename(chunk_path)}")
                    
                    self.log(f"自动识别：{original_name} ({total_chunks} 个分块)")
            
            if not chunk_files:
                self.log("错误：无法找到任何分块文件")
                self.update_status("未找到分块文件")
                return

            if output_dir is None:
                output_dir = file_dir

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            output_file = os.path.join(output_dir, original_name)

            self.log("-" * 60)
            self.log(f"合并文件：{original_name}")
            self.log(f"分块数量：{total_chunks}")
            self.log("-" * 60)

            with open(output_file, 'wb') as outfile:
                for i, chunk_path in enumerate(chunk_files, 1):
                    with open(chunk_path, 'rb') as chunk_file:
                        outfile.write(chunk_file.read())
                    self.log(f"[{i:03d}/{total_chunks}] 已合并：{os.path.basename(chunk_path)}")
                    self.update_status(f"合并进度：{i}/{total_chunks}")

            self.log("-" * 60)
            self.log(f"✓ 合并完成！输出文件：{os.path.basename(output_file)}")

            if expected_md5:
                self.log("验证文件完整性...")
                file_hash = hashlib.md5()
                with open(output_file, 'rb') as f:
                    while True:
                        chunk = f.read(8192)
                        if not chunk:
                            break
                        file_hash.update(chunk)

                if file_hash.hexdigest() == expected_md5:
                    self.log("✓ MD5 校验通过")
                else:
                    self.log("✗ MD5 校验失败，文件可能损坏")

            self.update_status("合并成功")
            messagebox.showinfo("成功", f"文件合并完成！\n{os.path.basename(output_file)}")

        except Exception as e:
            self.log(f"错误：{e}")
            import traceback
            self.log(traceback.format_exc())
            self.update_status("合并失败")

    def open_directory(self):
        if self.file_path.get():
            file_dir = os.path.dirname(self.file_path.get())
            if file_dir and os.path.exists(file_dir):
                os.startfile(file_dir)


def main():
    root = tk.Tk()
    app = FileSplitterGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
