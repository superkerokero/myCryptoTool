# myCryptoTool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 介绍

`myCryptoTool`是一个简单的基于Python和Tkinter的加密货币价格分析工具。
通过爬取[coinmarketcap.com](https://coinmarketcap.com/)上的加密货币价格信息来实现各种不同标准的排序功能。

![app_interface](img/app_interface.png)

目前支持的功能为按照以下标准对有记录的所有加密货币进行排序：

* 指定区间内高点对低点涨幅
* 现价相对于初始价涨幅
* 现价相对于历史低点涨幅
* 现价相对于指定期间低点涨幅

预计以后将会追加更多的功能。另外欢迎通过pull request的方式来为此app追加功能。

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