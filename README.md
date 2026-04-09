# Little Computer

一个适用于 Windows 的简洁计算器，支持以下功能：

- 加法、减法、乘法、除法
- 平方（x²）
- 平方根（√x）
- 倒数（1/x）
- 百分号（%）

界面采用黄绿色主题，风格参考系统计算器布局。

## 本地运行

1. 安装 Python 3.11+
2. 运行：

```powershell
python calculator.py
```

## 本地构建 EXE

```powershell
pip install pyinstaller
pyinstaller --clean --noconfirm calculator.spec
```

产物路径：

- `dist/LittleComputer.exe`

## 本地构建安装包（可选）

1. 安装 Inno Setup 6
2. 编译 `installer.iss`

产物路径：

- `Output/LittleComputerInstaller.exe`

## GitHub Actions 自动发布

仓库已配置 `.github/workflows/build-release.yml`：

- 手动触发：`workflow_dispatch`
- 自动触发：推送 tag（例如 `v1.0.0`）

触发后会自动：

1. 构建 `LittleComputer.exe`
2. 构建 `LittleComputerInstaller.exe`
3. 在 tag release 中上传上述文件
