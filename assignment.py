"""
Hourly_prices
"""
import csv


def get_data(file):
    """
    gets data from file
    """
    with open(file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def writer(file, data):
    """
    Writes data to file
    """
    with open(file, "w", encoding="utf-8") as f:
        fieldnames = ["Month", "Time", "Block", "Scalar"]
        dictwriter = csv.DictWriter(f, fieldnames=fieldnames)
        dictwriter.writeheader()
        for i in data:
            dictwriter.writerow(
                {
                    "Month": i["month"],
                    "Time": i["time"],
                    "Block": i["block"],
                    "Scalar": i["scalar"],
                }
            )


def calc_peak(month):
    """
    calculates peak energy block
    """
    peak = [float(i["price"]) for i in month if int(i["time"][:2]) in range(6, 22)]
    sum_price = sum(peak)
    total_prices = len(peak)
    return sum_price / total_prices


def calc_off_peak(month):
    """
    calculates off-peak energy block
    """
    block = [
        float(i["price"]) for i in month if int(i["time"][:2]) not in range(6, 22)
    ]
    sum_price = sum(block)
    total_prices = len(block)
    return sum_price / total_prices


def calc_scalar(data):
    """
    calculates energy scalar
    """
    for i in data:
        scalar = str(float(i["price"]) / float(i["block"]))
        i["scalar"] = scalar[: scalar.index(".") + 3]
        print(i)
        del i["price"]
    return data


def to_monthly(data):
    """
    converts daily data to monthly data
    """
    dicn = {}
    for i in data:
        if i["date"][11:] not in dicn:
            dicn[i["date"][11:]] = []
        dicn[i["date"][11:]].append(float(i["price"]))
    for j in dicn:
        avg = str(sum(dicn[j]) / len(dicn[j]))
        dicn[j] = avg[: avg.index(".") + 3]
    return dicn


def answer():
    """
    answer function
    """
    daily_data = get_data("hourly_prices.csv")
    monthwise = []
    for i in range(1, 13):
        monthly = []
        for j in daily_data:
            if int(j["date"][5:7]) == i:
                monthly.append(j)
        month_data = to_monthly(monthly)
        for k in month_data:
            monthwise.append({"month": i, "time": k, "price": month_data[k]})

    block_data = []
    for i in range(1, 13):
        months = []
        for j in monthwise:
            if j["month"] == i:
                months.append(j)
        month_peak = str(calc_peak(months))
        month_off_peak = str(calc_off_peak(months))
        for k in months:
            if int(k["time"][:2]) in range(6, 22):
                k["block"] = month_peak[: month_peak.index(".") + 3]
            else:
                k["block"] = month_off_peak[: month_off_peak.index(".") + 3]
        block_data.extend(months)

    data = calc_scalar(block_data)
    writer("answer.csv", data)

answer()