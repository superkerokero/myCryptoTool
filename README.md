# myCryptoTool
A GUI tool based on python/tkinter for cryptocurrency price analysis.

## 安装及运行

本app支持的Python版本为3.4及以上。

```bash
# 下载并安装依存库
git clone https://github.com/superkerokero/myCryptoTool.git
cd myCryptoTool
pip install -r requirements.txt

# 运行app
cd src
python app.py
```


## 使用pyinstaller打包为独立可执行文件

在确定已经安装pyinstaller的前提下，移动至src目录下执行如下命令：
```bash
pyinstaller --onefile --additional-hooks-dir=. app.py
```
然后将src下的data文件夹拷贝至dist/app文件夹下，即可得到可独立执行的exe文件。