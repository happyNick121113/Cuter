# 📦 File Splitter - GitHub 文件分割工具

一个纯前端的浏览器文件分割与合并工具，帮助突破 GitHub 25MB 单文件限制。

## ✨ 功能特性

- 🎯 **文件分割** - 将大文件分割成多个小块（默认 24MB）
- 🔗 **文件合并** - 自动识别并合并分块文件
- 📦 **ZIP 打包** - 分割后自动打包为 ZIP 文件下载
- 🔒 **MD5 校验** - 支持文件完整性验证（SHA-256）
- 🖱️ **拖拽支持** - 支持拖拽文件上传
- 🌐 **纯前端** - 无需安装，浏览器即可使用
- 🎨 **精美界面** - 现代化渐变 UI 设计

## 🚀 使用方法

### 分割文件

1. 打开 `cuter.html` 文件
2. 选择"✂️ 分割文件"模式
3. 点击文件选择区域或拖拽文件到此处
4. 设置分块大小（推荐 24MB，适合 GitHub）
5. 点击"开始分割"按钮
6. 等待处理完成，自动下载 ZIP 文件

### 合并文件

1. 选择"🔗 合并文件"模式
2. 选择包含所有分块文件的文件夹
3. 点击"开始合并"按钮
4. 程序会自动：
   - 查找 `.splitinfo` 信息文件
   - 或自动识别分块命名模式
   - 合并所有分块
   - 验证文件完整性（如有 MD5）
5. 自动下载合并后的完整文件

## 📋 分块文件命名规则

分割后的文件命名格式：
```
原文件名_1
原文件名_2
原文件名_3
...
```

同时会生成一个 `.splitinfo` 信息文件，包含：
- 原始文件名
- 文件总大小
- 分块大小
- 分块数量
- MD5 哈希值（用于完整性验证）

## ⚙️ 配置选项

### 分块大小

- **默认值**：24 MB
- **推荐范围**：1-100 MB
- **GitHub 安全值**：24 MB（低于 25MB 限制）

### 文件校验

合并时会自动进行 MD5 校验（如果存在 `.splitinfo` 文件），确保文件完整性。

## 🛠️ 技术栈

- **HTML5** - 文件 API、拖拽 API
- **CSS3** - 渐变背景、响应式设计
- **JavaScript** - 异步处理、文件操作
- **JSZip** - ZIP 文件生成
- **FileSaver.js** - 文件下载

## 📦 依赖库

通过 CDN 加载：
- [JSZip 3.10.1](https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js) - ZIP 文件处理
- [FileSaver.js 2.0.5](https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/2.0.5/FileSaver.min.js) - 文件保存

## 💡 使用场景

### 适用于

- ✅ 上传大文件到 GitHub 仓库
- ✅ 通过邮件发送大文件（超过附件限制）
- ✅ 网盘分块上传
- ✅ 备份文件分割存储

### 优势

- 🔒 **隐私安全** - 所有操作在本地浏览器完成，不上传服务器
- ⚡ **快速处理** - 利用浏览器多线程处理
- 💾 **无需安装** - 打开 HTML 文件即可使用
- 🌍 **跨平台** - 支持 Windows、macOS、Linux

## ⚠️ 注意事项

1. **内存限制** - 处理超大文件时，确保浏览器有足够内存
2. **文件格式** - 支持任意类型的文件
3. **浏览器要求** - 需要现代浏览器（Chrome、Firefox、Edge、Safari）
4. **网络环境** - CDN 资源需要网络连接首次加载

##  示例

### 分割 100MB 文件

```
输入：video.mp4 (100MB)
分块大小：24MB
输出：
  - video.mp4_1 (24MB)
  - video.mp4_2 (24MB)
  - video.mp4_3 (24MB)
  - video.mp4_4 (24MB)
  - video.mp4_5 (4MB)
  - video.mp4.splitinfo
打包：video.mp4_parts.zip
```

### 合并分块

```
输入文件夹包含：
  - video.mp4_1
  - video.mp4_2
  - video.mp4_3
  - video.mp4_4
  - video.mp4_5
  - video.mp4.splitinfo
  
输出：video.mp4 (100MB)
校验：✓ MD5 验证通过
```

## 📝 更新日志

### v1.0.0 (2026-04-17)
- ✨ 初始版本发布
- ✨ 文件分割功能
- ✨ 文件合并功能
- ✨ ZIP 打包下载
- ✨ MD5 完整性校验
- ✨ 拖拽上传支持
- ✨ 实时进度显示
- ✨ 日志记录功能

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [JSZip](https://github.com/Stuk/jszip) - 强大的 JavaScript ZIP 库
- [FileSaver.js](https://github.com/eligrey/FileSaver.js) - 文件保存解决方案

---

**提示**：本项目完全在浏览器本地运行，所有文件处理均在您的设备上完成，不会上传到任何服务器。
