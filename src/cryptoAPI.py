from coinmarketcap import Market
from cryptocmd import CmcScraper
import json
import pandas as pd


def get_history_all():
    """Get all history close data."""
    cmc = Market()
    listing = [item['symbol'] for item in cmc.listings()['data']]
    ret = dict()
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
            ret[x] = dict(
                t=ti,
                p=pr
            )
        except Exception:
            print("Invalid coin ssymbol: {0}".format(x))
        print(i, x)
    return ret


def get_id_table():
    """Get a dictionary from symbol to id."""
    sym2id = dict()
    id2sym = dict()
    cmc = Market()
    for i, x in enumerate(cmc.listings()["data"]):
        sym2id[x["symbol"]] = x["id"]
        id2sym[x["id"]] = x["symbol"]
    return sym2id, id2sym


def save_history(fname):
    """Save history data to a json file."""
    hist = get_history_all()
    s2i, i2s = get_id_table()
    outdata = dict(
        history=hist,
        s2i=s2i,
        i2s=i2s
    )
    with open(fname, "w") as f:
        json.dump(outdata, f)


def load_history(fname):
    """Save history data to a json file."""
    with open(fname, "r") as f:
        ret = json.load(f)
    return ret['history'], ret['s2i'], ret['i2s']


def get_current_price(cid):
    """Return current price of the coin from coinmarketcap."""
    cmc = Market()
    return cmc.ticker(cid)["data"]["quotes"]["USD"]["price"]


def sort_by_mode(hist, st, et, mode):
    """Sort price data by section."""
    ret = list()
    for key, val in hist.items():
        try:
            ist = val["t"].index(st)
        except ValueError:
            ist = -1
        try:
            iet = val["t"].index(et)
        except ValueError:
            iet = 0
        if ist == -1:
            high_price = max(val["p"][iet:]) 
            low_price = min(val["p"][iet:])
        else:
            high_price = max(val["p"][iet:ist+1]) 
            low_price = min(val["p"][iet:ist+1])
        high_price_all = max(val["p"])
        low_price_all = min(val["p"])
        ret.append((key, val["p"][-1], val["p"][0], high_price_all,
                    low_price_all, high_price, low_price,
                    (val["p"][0] - val["p"][-1]) / val["p"][-1], 
                    (val["p"][0] - low_price_all) / low_price_all,
                    (val["p"][0] - low_price) / low_price,
                    (high_price - low_price) / low_price))
    if mode == 0:
        ret.sort(key=lambda x: x[-1], reverse=True)
    elif mode == 1:
        ret.sort(key=lambda x: x[7], reverse=True)
    elif mode == 2:
        ret.sort(key=lambda x: x[8], reverse=True)
    elif mode == 3:
        ret.sort(key=lambda x: x[9], reverse=True)
    else:
        pass
    return ret


def make_df(data):
    """Create a DataFrame object from given data."""
    df = pd.DataFrame(data, columns=["币种", "起始价格", "当前价格", "历史最高价格", "历史最低价格",
                                     "区间最高价格", "区间最低价格", "现价相对初始价涨幅",
                                     "现价相对历史最低价涨幅", "现价相对区间最低价涨幅",
                                     "区间内最高价相对最低价涨幅"])
    return df
