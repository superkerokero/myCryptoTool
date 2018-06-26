import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from coinmarketcap import Market
from cryptocmd import CmcScraper
import json
from cryptoAPI import load_history, sort_by_mode, make_df, get_id_table


def toCSV(event):
    fname = fn.get()+".csv"
    try:
        hist, s2i, i2s = load_history("cmc_history.json")
        df = make_df(sort_by_mode(hist, st.get(), et.get(), opt.get()))
        df.to_csv(fname)
        messagebox.showinfo('info', "成功输出文件: {0}".format(fname))
    except ValueError:
        messagebox.showinfo('info', "数值错误，请检查输入区间是否合法")
    except:
        messagebox.showinfo('info', "系统错误，如果第一次打开本app，请先点击右下角“更新数据”按钮进行数据更新")


def toExcel(event):
    fname = fn.get()+".xlsx"
    try:
        hist, s2i, i2s = load_history("cmc_history.json")
        df = make_df(sort_by_mode(hist, st.get(), et.get(), opt.get()))
        writer = pd.ExcelWriter(fname)
        df.to_excel(writer, 'Sheet1')
        writer.save()
        messagebox.showinfo('info', "成功输出文件: {0}".format(fname))
    except ValueError:
        messagebox.showinfo('info', "数值错误，请检查输入区间是否合法")
    except:
        messagebox.showinfo('info', "系统错误，如果第一次打开本app，请先点击右下角“更新数据”按钮进行数据更新")


def update(event):
    messagebox.showinfo('info',
                        """更新历史数据耗时较久，视网络环境需时20到40分钟，
                        输出文件名下方的进度条显示当前的更新进度，
                        背后的命令行窗口会输出目前处理中的加密货币ID和符号，
                        coinmarkectcap目前共有1500多种加密货币""")
    cmc = Market()
    listing = [item['symbol'] for item in cmc.listings()['data']]
    hist = dict()
    step = 100 / len(listing)
    for i, x in enumerate(listing):
        scr = CmcScraper(x)
        try:
            header, data = scr.get_data()
            ti = list()
            pr = list()
            for j, xx in enumerate(data):
                if xx[4]:
                    pr.append(xx[4])
                    ti.append(xx[0])
            hist[x] = dict(
                t=ti,
                p=pr
            )
        except Exception:
            print("Invalid coin ssymbol: {0}".format(x))
        print(i, x)
        progress.step(step)
        progress.update()
    sym2id, id2sym = get_id_table()
    outdata = dict(
        history=hist,
        s2i=sym2id,
        i2s=id2sym
    )
    with open("cmc_history.json", "w") as f:
        json.dump(outdata, f)
    messagebox.showinfo('info', "成功更新历史数据")


root = tk.Tk()
root.title("myCryptoTool")
root.geometry("200x270")

tk.Label(root, text="开始时间", foreground='#000000', background='#ffaacc').pack()

st = tk.StringVar()
tk.Entry(root, width=10, textvariable=st).pack()
st.set("01-04-2018")

tk.Label(root, text="终止时间", foreground='#000000', background='#ffffcc').pack()

et = tk.StringVar()
tk.Entry(root, width=10, textvariable=et).pack()
et.set("01-05-2018")

opt = tk.IntVar()
tk.Radiobutton(root,
               text="指定区间内高点对低点涨幅", variable=opt, value=0).pack(anchor=tk.W)
tk.Radiobutton(root,
               text="现价相对于初始价涨幅", variable=opt, value=1).pack(anchor=tk.W)
tk.Radiobutton(root,
               text="现价相对于历史低点涨幅", variable=opt, value=2).pack(anchor=tk.W)
tk.Radiobutton(root,
               text="现价相对于指定期间低点涨幅", variable=opt, value=3).pack(anchor=tk.W)

tk.Label(root, text="输出文件名(app根目录下)", foreground='#000000',
         background='#aaaaff').pack()
fn = tk.StringVar()
tk.Entry(root, width=50, textvariable=fn).pack()
fn.set("output")

progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=200)
progress.pack(fill=tk.X, padx=20)

btn1 = tk.Button(root, text="输出csv")
btn1.bind("<Button-1>", toCSV)
btn1.pack(side=tk.LEFT)

btn2 = tk.Button(root, text="输出excel")
btn2.bind("<Button-1>", toExcel)
btn2.pack(side=tk.LEFT)

btn3 = tk.Button(root, text="更新数据")
btn3.bind("<Button-1>", update)
btn3.pack(side=tk.RIGHT)

root.mainloop()