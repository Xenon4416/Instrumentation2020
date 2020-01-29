Months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def compareDate(val1, val2):
    if val2[2] > val1[2]:
        return 1
    elif val2[2] < val1[2]:
        return -1
    elif val2[0] > val1[0]:
        return 1
    elif val2[0] < val1[0]:
        return -1
    elif val2[1] > val1[1]:
        return 1
    elif val2[1] < val1[1]:
        return -1
    else:
        return 0


def autoLabel(rects,ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def CalculateAllDataForSummary(values):
    summaryData = [[[],[],[],[]],[[],[],[]]]
    for i in values:
        temp = [str(i[1][0]) + ':' + str((i[1][1] // 10) * 10) + i[2], i[3]]
        updateData(temp, summaryData[0][0])
        temp = [Months[i[0][0]-1] + ' ' + str(i[0][1]) + ',' + str(i[1][0]) + i[2], i[3]]
        updateData(temp, summaryData[0][1])
        temp = [Months[i[0][0]-1] + ' ' + str(i[0][1]), i[3]]
        updateData(temp, summaryData[0][2])
        temp = [Months[i[0][0]-1] + ' ' + str(i[0][2]), i[3]]
        updateData(temp, summaryData[0][3])
        temp = [str(i[1][0]) + i[2], i[3]]
        updateData(temp, summaryData[1][0])
        temp = [str(i[0][1]), i[3]]
        updateData(temp, summaryData[1][1])
        temp = [Months[i[0][0]-1], i[3]]
        updateData(temp, summaryData[1][2])
    return summaryData


def updateData(temp, data):
    datX = [j[0] for j in data]
    if temp[0] not in datX:
        if temp[1]:
            data.append([temp[0], 1, 0])
        else:
            data.append([temp[0], 0, 1])
    else:
        if temp[1]:
            data[datX.index(temp[0])][1] += 1
        else:
            data[datX.index(temp[0])][2] += 1


# def compareDateTime(val1, val2):
#     if compareDate(val1, val2) != 0:
#         return compareDate(val1, val2)
#     else:
#         if val2[2] == 'PM' and val1[2] == 'AM':
#             return 1
#         elif val2[2] == 'AM' and val1[2] == 'PM':
#             return -1
#         elif val2[1][0] != 12 and val1[1][0] == 12:
#             return 1
#         elif val2[1][0] == 12 and val1[1][0] != 12:
#             return -1
#         elif val2[1][0] > val1[1][0]:
#             return 1
#         elif val2[1][0] < val1[1][0]:
#             return -1
#         elif val2[1][1] > val1[1][1]:
#             return 1
#         elif val2[1][1] < val1[1][1]:
#             return -1
#         elif val2[1][2] > val1[1][2]:
#             return 1
#         elif val2[1][2] < val1[1][2]:
#             return -1
#         else:
#             return 0


if __name__ == '__main__':
    pass
