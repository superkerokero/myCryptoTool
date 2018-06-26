import tkinter as tk
from tkinter import messagebox
import pandas as pd
from cryptoAPI import load_history, sort_by_mode, make_df


def toCSV(event):
    fname = fn.get()+".csv"
    try:
        hist, s2i, i2s = load_history("data/cmc_history.json")
        df = make_df(sort_by_mode(hist, st.get(), et.get(), opt.get()))
        df.to_csv(fname)
        messagebox.showinfo('info', "成功输出文件: {0}".format(fname))
    except ValueError:
        messagebox.showinfo('info', "数值错误， 请检查输入区间是否合法")
    except:
        messagebox.showinfo('info', "未知错误")


def toExcel(event):
    fname = fn.get()+".xlsx"
    try:
        hist, s2i, i2s = load_history("data/cmc_history.json")
        df = make_df(sort_by_mode(hist, st.get(), et.get(), opt.get()))
        writer = pd.ExcelWriter(fname)
        df.to_excel(writer, 'Sheet1')
        writer.save()
        messagebox.showinfo('info', "成功输出文件: {0}".format(fname))
    except ValueError:
        messagebox.showinfo('info', "数值错误， 请检查输入区间是否合法")
    except:
        messagebox.showinfo('info', "未知错误")


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

tk.Label(root, text="输出文件名", foreground='#000000', background='#aaaaff').pack()
fn = tk.StringVar()
tk.Entry(root, width=50, textvariable=fn).pack()
fn.set("output")

btn1 = tk.Button(root, text="输出csv文件")
btn1.bind("<Button-1>", toCSV)
btn1.pack()

btn2 = tk.Button(root, text="输出excel文件")
btn2.bind("<Button-1>", toExcel)
btn2.pack()

root.mainloop()