# QuickInput - 快速输入工具

一个现代化的快速文本输入工具，通过热键快速弹出选择窗口，支持预设文本的快速输入。

## 🚀 功能特点

- **快捷热键**: 使用 `Ctrl+[` 快速调出输入窗口
- **现代化界面**: 美观的深色主题界面设计
- **系统托盘**: 后台运行，通过系统托盘管理
- **智能焦点**: 自动获取键盘焦点，无需手动点击
- **快速输入**: 按数字键1-9快速输入预设文本
- **可定制**: 通过CSV文件轻松配置文本内容

## 📸 界面预览

- **弹窗界面**: 现代化的深色主题，清晰的按键提示
- **悬停效果**: 鼠标悬停时的高亮显示
- **系统托盘**: 简洁的托盘图标和菜单

## 🛠️ 安装指南

### 1. 环境要求

- Python 3.7+
- Windows 操作系统

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行程序

```bash
python main.py
```

## 📝 使用说明

### 基本使用

1. **启动程序**: 双击运行 `main.py` 或在命令行中执行
2. **后台运行**: 程序会在系统托盘中显示图标
3. **调出窗口**: 使用热键 `Ctrl+[` 调出快速输入窗口
4. **选择文本**: 按数字键 1-9 选择对应的预设文本
5. **自动输入**: 程序会自动输入选中的文本到当前光标位置

### 自定义文本内容

编辑 `text.csv` 文件来自定义你的预设文本：

```csv
key,text
1,Welcome to our website!
2,Thank you for your visit.
3,Please contact us at: contact@example.com
4,Check out our latest blog post.
5,Subscribe to our newsletter for updates.
6,Learn more about our services here.
7,Follow us on social media.
8,Visit our FAQ page for more information.
9,Click here to see our latest offers.
```

### 快捷键

- `Ctrl+[`: 调出快速输入窗口
- `1-9`: 选择对应的预设文本
- `ESC`: 关闭弹窗窗口

## 🔧 技术架构

### 核心组件

- **QuickInputApp**: 主应用程序类
- **GUI界面**: 基于tkinter的现代化界面
- **热键监听**: 使用pynput监听全局热键
- **系统托盘**: 使用pystray管理托盘图标
- **文本输入**: 使用pyautogui模拟键盘输入

### 依赖包

- `tkinter`: GUI界面框架
- `pillow`: 图像处理
- `pyautogui`: 自动化输入
- `pywin32`: Windows API调用
- `pystray`: 系统托盘管理
- `pynput`: 全局热键监听

## 🎨 界面设计

### 颜色方案

- **背景色**: `#2c3e50` (深蓝灰色)
- **选项背景**: `#34495e` (中性灰色)
- **悬停色**: `#3498db` (蓝色)
- **按键标签**: `#e74c3c` (红色)
- **文字颜色**: `#ecf0f1` (浅灰白色)

### 字体设计

- **主标题**: Segoe UI, 16px, 粗体
- **副标题**: Segoe UI, 10px, 常规
- **选项文本**: Segoe UI, 10px, 常规

## 🐛 故障排除

### 常见问题

1. **热键不响应**
   - 检查是否有其他程序占用了 `Ctrl+[` 热键
   - 以管理员权限运行程序

2. **弹窗无法获取焦点**
   - 程序已经自动处理了焦点问题
   - 如果仍有问题，请重启程序

3. **中文乱码**
   - 程序已经修复了Windows控制台的中文乱码问题
   - 确保系统支持UTF-8编码

4. **系统托盘图标不显示**
   - 检查是否有 `icon.png` 文件
   - 程序会自动生成默认图标

### 日志查看

程序运行时会输出详细的日志信息，包括：
- 文本加载状态
- 热键设置状态
- 窗口创建和关闭状态
- 错误和警告信息

## 📁 文件结构

```
QuickInput/
├── main.py              # 主程序文件
├── text.csv             # 文本配置文件
├── icon.png             # 应用图标
├── requirements.txt     # 依赖包列表
├── README.md           # 项目文档
└── LICENSE             # 许可证文件
```

## 🔄 版本历史

### v2.0.0 (当前版本)
- ✨ 全新的现代化界面设计
- 🔧 重构了代码架构，提高了可维护性
- 🐛 修复了窗口焦点问题
- 🌐 修复了中文乱码问题
- 📝 添加了完整的日志记录
- 🎨 改进了用户体验

### v1.0.0 (原始版本)
- 基本的快速输入功能
- 简单的GUI界面
- 热键支持

## 📄 许可证

本项目使用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

### 开发环境设置

1. 克隆仓库
2. 安装依赖: `pip install -r requirements.txt`
3. 运行程序: `python main.py`

### 代码规范

- 使用Python 3.7+语法
- 遵循PEP 8代码规范
- 添加适当的注释和文档字符串
- 测试所有功能

## 📞 联系方式

如有任何问题，请通过以下方式联系：

- 提交Issue到GitHub仓库
- 邮件联系（如有提供）

---

*让文本输入更加高效！* 🚀 