import wx
import wx.adv as adv
import matplotlib.pyplot as plt
import numpy as np
import BasicFuncions as BFuns


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame("Crowd Analyzer", (50, 60), (800, 600))
        # frame.SetBackgroundColour((150,150,150))
        frame.Show()
        self.SetTopWindow(frame)
        return True


class MyFrame(wx.Frame):
    def __init__(self, title, pos, size):
        wx.Frame.__init__(self, None, -1, title, pos, size, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
        self.panel = wx.Panel(self, -1)
        self.fig = []
        self.axes = []
        self.InitialSetup()
        # self.count = 0
        # self.gauge = wx.Gauge(self.panel, -1, 50, (20, 50), (250, 25))
        # self.gauge.SetBezelFace(3)
        # self.gauge.SetShadowWidth(3)
        # self.Bind(wx.EVT_IDLE, self.OnIdle)

    def InitialSetup(self):
        self.counts = self.LoadFile()
        self.CreateStatusBar()
        self.SetStatusText("Welcome to wxPython!")
        self.CreateMenuBar()
        self.AddDateSelectors()
        self.AddPlotSelector()
        self.AddSamplingSelector()
        self.AddDataSetSelector()
        self.AddIntervalSelector()
        self.AddPlotButtons()
        self.BindEvents()
        self.From.SetDate(wx.DateTime(self.values[0][0][1], self.values[0][0][0]-1, self.values[0][0][2]))
        self.To.SetDate(wx.DateTime(self.values[-1][0][1], self.values[-1][0][0] - 1, self.values[-1][0][2]))
        self.ShowSampleStats()

    def ShowPlot(self, source):
        if source == 'plotButton':
            # for i in self.fig:
            #     plt.close(i)
            plt.close('all')
            self.fig = []
            self.axes = []
        totalAxes = len(self.axes)
        if totalAxes != 4:
            self.fig.append(plt.figure())
            self.axes.append(self.fig[totalAxes].add_subplot(111))
        else:
            wx.MessageBox('Plot Limit Info', 'Maximum simultaneous plot limit reached', wx.OK | wx.ICON_INFORMATION, self)
            return
        axis = self.axes[totalAxes]
        self.data = []
        temp = str(self.From.GetDate()).split(' ')
        dateRange = [[int(i) for i in temp[0].split('/')]]
        temp = str(self.To.GetDate()).split(' ')
        dateRange.append([int(i) for i in temp[0].split('/')])
        intrvl = self.intervals[self.interval.GetSelection()]
        for i in self.values:
            if BFuns.compareDate(dateRange[0], i[0]) >= 0 >= BFuns.compareDate(dateRange[1], i[0]):
                if self.samplings[self.sampling.GetSelection()] == 'Unique':
                    self.UniqueModeSampling(intrvl, i)
                else:
                    self.CommonModeSampling(intrvl, i)
        if self.data:
            self.PlotResult(axis)
        else:
            wx.MessageBox("There is no data in between the date range", "Plot Information", wx.OK | wx.ICON_INFORMATION, self)

        # data = [self.values[i][1][1] for i in range(len(self.values))]
        # dataX = [i for i in range(6)]
        # dataY = [0 for i in range(6)]
        # for i in data:
        #     dataY[i//10] += 1
        # fig = plt.plot(dataX, dataY)
        # plt.show()
        # print(intrvl)

    def UniqueModeSampling(self, intrvl, i):
        if intrvl == '10 Minute':
            # temp = [i[0], [i[1][0], i[1][1]//10, i[1][2]], i[2], i[3]]
            temp = [str(i[1][0]) + ':' + str((i[1][1] // 10) * 10) + i[2], i[3]]
            self.xLabel = '10 Minutes Interval Time'
        elif intrvl == 'Hour':
            # temp = [i[0], i[1][0], i[2], i[3]]
            temp = [BFuns.Months[i[0][0]-1] + ' ' + str(i[0][1]) + ',' + str(i[1][0]) + i[2], i[3]]
            self.xLabel = '1 Hour Interval Time'
        elif intrvl == 'Day':
            # temp = [i[0], i[-1]]
            temp = [BFuns.Months[i[0][0]-1] + ' ' + str(i[0][1]), i[3]]
            self.xLabel = '1 Day Interval Time'
        elif intrvl == 'Month':
            # temp = [[i[0][1], i[0][2]], i[-1]]
            temp = [BFuns.Months[i[0][0]-1] + ' ' + str(i[0][2]), i[3]]
            self.xLabel = '1 Month Interval Time'
        BFuns.updateData(temp, self.data)

    def CommonModeSampling(self, intrvl, i):
        if intrvl == '10 Minute':
            temp = [str(i[1][0]) + ':' + str((i[1][1] // 10) * 10) + i[2], i[3]]
            self.xLabel = '10 Minutes Interval Time'
        elif intrvl == 'Hour':
            temp = [str(i[1][0]) + i[2], i[3]]
            self.xLabel = '1 Hour Interval Time'
        elif intrvl == 'Day':
            temp = [str(i[0][1]), i[3]]
            self.xLabel = '1 Day Interval Time'
        elif intrvl == 'Month':
            temp = [BFuns.Months[i[0][0]-1], i[3]]
            self.xLabel = '1 Month Interval Time'
        BFuns.updateData(temp, self.data)

    def AnalyzeSummary(self):
        summaryData = BFuns.CalculateAllDataForSummary(self.values)
        analyzedSummary = []
        for i in summaryData:
            out2 = []
            for j in i:
                temp = j[:]
                inContent  = []
                outContent = []
                tempIn = [k[1] for k in j]
                tempOut = [k[2] for k in j]
                maxIn = max(tempIn)
                if maxIn:
                    while maxIn in tempIn:
                        inContent.append(temp[tempIn.index(maxIn)][0])
                        temp.pop(tempIn.index(maxIn))
                        tempIn.remove(maxIn)
                temp = j[:]
                maxOut = max(tempOut)
                if maxOut:
                    while maxOut in tempOut:
                        outContent.append(temp[tempOut.index(maxOut)][0])
                        temp.pop(tempOut.index(maxOut))
                        tempOut.remove(maxOut)
                out1 = [[inContent, maxIn], [outContent, maxOut]]
                out2.append(out1)
            analyzedSummary.append(out2)
        return analyzedSummary

    def PlotResult(self, axis):
        plotsel = self.plots[self.plot.GetSelection()]
        dataset = self.datasets[self.dataset.GetSelection()]
        tempDAT = []
        # Filtering empty entries in case of either plot
        if dataset == 'Entry':
            for i in range(len(self.data)):
                if self.data[i][1] != 0:
                    tempDAT.append(self.data[i])
            self.data = tempDAT
        elif dataset == 'Exit':
            for i in range(len(self.data)):
                if self.data[i][2] != 0:
                    tempDAT.append(self.data[i])
            self.data = tempDAT
        if plotsel == 'Line':
            if dataset == 'Entry' or dataset == 'Both':
                axis.plot([i[0] for i in self.data], [i[1] for i in self.data], label='Entry')
            if dataset == 'Exit' or dataset == 'Both':
                axis.plot([i[0] for i in self.data], [i[2] for i in self.data], label='Exit')
            axis.set(xlabel=self.xLabel, ylabel='Frequency Reference')
        elif plotsel == 'Bar':
            if dataset == 'Entry':
                ax1 = axis.bar([i[0] for i in self.data], [i[1] for i in self.data], label='Entry')
                BFuns.autoLabel(ax1, axis)
            elif dataset == 'Exit':
                ax2 = axis.bar([i[0] for i in self.data], [i[2] for i in self.data], label='Exit')
                BFuns.autoLabel(ax2, axis)
            else:
                width = 0.35
                index = np.arange(len(self.data))
                ax1 = axis.bar(index-width/2, [i[1] for i in self.data], label='Entry', width=width)
                BFuns.autoLabel(ax1, axis)
                ax2 = axis.bar(index+width/2, [i[2] for i in self.data], label='Entry', width=width)
                BFuns.autoLabel(ax2, axis)
                axis.set_xticks(index)
                axis.set_xticklabels([i[0] for i in self.data])
            axis.set(xlabel=self.xLabel, ylabel='Frequency Reference')
        elif plotsel == 'Pie':
            if dataset == 'Entry':
                axis.pie([i[1] for i in self.data], labels=[i[0] for i in self.data],
                        explode=[0.02 for i in range(len(self.data))])
            elif dataset == 'Exit':
                axis.pie([i[2] for i in self.data], labels=[i[0] for i in self.data],
                        explode=[0.02 for i in range(len(self.data))])
            else:
                wx.MessageBox("More than one data cannot be plot in PieChart", "Pie Plot Info", wx.OK | wx.ICON_INFORMATION, self)
                return
        if plotsel != 'Pie':
            axis.legend()
        plt.rc('axes', axisbelow=True)
        # axis.rcParams['axes.axisbelow'] = True
        plt.grid(True, linestyle='--', alpha=0.5, zorder=1)
        axis.set_title('Crowd Frequency Data')
        plt.show()

    def OnPlot(self, event):
        self.ShowPlot(event.GetEventObject().GetName())

    def OnAddToPlot(self, event):
        self.ShowPlot(event.GetEventObject().GetName())

    def AddIntervalSelector(self):
        self.intervals = ['10 Minute', 'Hour', 'Day', 'Month']
        self.interval = wx.RadioBox(self.panel, -1, "Interval Selection", (270, 15), wx.DefaultSize, self.intervals, 2, wx.RA_SPECIFY_COLS)

    def AddPlotSelector(self):
        self.plots = ['Line', 'Bar', 'Pie']
        self.plot = wx.RadioBox(self.panel, -1, "Plot Selection", (270, 105), (165,53), self.plots, 3, wx.RA_SPECIFY_COLS)

    def AddSamplingSelector(self):
        self.samplings = ['Unique', 'Common']
        self.sampling = wx.RadioBox(self.panel, -1, "Sampling Mode", (270, 175), (165,53), self.samplings, 2, wx.RA_SPECIFY_COLS)

    def AddDataSetSelector(self):
        self.datasets = ['Entry', 'Exit', 'Both']
        self.dataset = wx.RadioBox(self.panel, -1, "DataSet", (270, 245), (165,53), self.datasets, 3, wx.RA_SPECIFY_COLS)

    def AddPlotButtons(self):
        self.plotButton = wx.Button(self.panel, -1, "Plot", pos=(300, 350), name='plotButton')
        self.addPlotButton = wx.Button(self.panel, -1, "Add to Plot", pos=(300, 310), name='addPlotButton')
        self.plotButton.SetFocus()

    def LoadFile(self):
        result = [0, 0, 0]
        self.values = []
        self.usageInfo = open('Guide.txt').read()
        data = [lines.strip() for lines in open('Data.txt')]
        # for i in range(len(data)):
        #     temp = []
        #     temp.append((int(data[i][:2]), int(data[i][3:5]), int(data[i][6:10])))
        #     temp.append((int(data[i][11:13]), int(data[i][14:16]), int(data[i][17:19])))
        #     temp.append(data[i][20:22])
        #     temp.append(int(data[i][23]))
        #     self.values.append(temp)
        for i in range(len(data)):
            temp = []
            temp1 = data[i].split(' ')
            temp2 = temp1[0].split('/')
            temp3 = temp1[1].split(':')
            temp.append([int(i) for i in temp2])
            temp.append([int(i) for i in temp3])
            temp.append(temp1[2])
            temp.append(int(temp1[3]))
            self.values.append(temp)
            result[0] += 1
            if self.values[i][3]:
                result[1] += 1
            else:
                result[2] += 1
        return result

    def ReloadStaticText(self):
        self.RefreshStaticTexts()
        for i in range(len(self.sampleStats)):
            self.sampleStats[i].SetLabel(self.staticTexts[i][0])

    def AddDateSelectors(self):
        wx.StaticText(self.panel, -1, "Data Representation Date From :", (30, 15))
        self.From = adv.CalendarCtrl(self.panel, -1, pos=(20, 25))
        self.From.SetBackgroundColour((0,180,0))
        wx.StaticText(self.panel, -1, "Data Representation Date To :", (30, 205))
        self.To = adv.CalendarCtrl(self.panel, -1, pos=(20, 215))
        self.To.SetBackgroundColour((0, 180, 0))

    def CreateMenuBar(self):
        self.menuFile = wx.Menu()
        self.menuFile.Append(1, "&Reload Data")
        self.menuFile.Append(2, "&About...")
        self.menuFile.AppendSeparator()
        self.menuFile.Append(3, "E&xit")
        self.menuFile2 = wx.Menu()
        self.menuFile2.Append(4, 'Usage Guide')
        self.menuBar = wx.MenuBar()
        self.menuBar.Append(self.menuFile, "&File")
        self.menuBar.Append(self.menuFile2, '&Help')
        self.SetMenuBar(self.menuBar)

    def ShowSampleStats(self):
        self.sampleStats = []
        self.RefreshStaticTexts()
        fontH1 = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, True)
        fontH2 = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, True)
        fontH3 = wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, True)
        for i in self.staticTexts:
            self.sampleStats.append(wx.StaticText(self.panel, -1, i[0], i[1]))
        for i in [0, 5]:
            self.sampleStats[i].SetForegroundColour((75, 75, 75))
            self.sampleStats[i].SetFont(fontH1)
        for i in [6, 19]:
            self.sampleStats[i].SetFont(fontH2)
            self.sampleStats[i].SetForegroundColour((50,50,50))
        for i in [7, 10, 13, 16, 20, 23, 26]:
            self.sampleStats[i].SetFont(fontH3)

    def RefreshStaticTexts(self):
        self.staticTexts = [["Total Sample Count : " + str(self.counts[0]), (20, 385)],
                            ["Total Entry Count : " + str(self.counts[1]), (20, 405)],
                            ["Total Exit Count : " + str(self.counts[2]), (20, 425)],
                            ["Sample From : " + str(str(self.From.GetDate()).split(' ')[0]), (20, 445)],
                            ["Sample To : " + str(str(self.To.GetDate()).split(' ')[0]), (20, 465)],
                            ["Sample Data Analysis :", (455, 15)]]
        pos = 35
        heads = [['Unique ', 'Common '], ['10 Min ', 'Hour ', 'Day ', 'Month '], [' InFlow : ', ' OutFow : ']]
        vals = self.AnalyzeSummary()
        for i in range(len(heads[0])):
            self.staticTexts.append([heads[0][i]+'Mode Sampling :', (455, pos)])
            pos += 20
            for j in range(len(heads[1])):
                if i == 1 and j == 0:
                    pass
                else:
                    self.staticTexts.append([heads[1][j] + 'Sampling :', (465, pos)])
                    pos += 20
                    for k in range(len(heads[2])):
                        l = j
                        if i == 1:
                            l = j - 1
                        self.staticTexts.append(
                            ['Max' + heads[2][k] + str(vals[i][l][k][0]) + ' : ' + str(vals[i][l][k][1]), (475, pos)])
                        pos += 20

    def BindEvents(self):
        self.Bind(wx.EVT_MENU, self.OnReload, id=1)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=2)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=3)
        self.Bind(wx.EVT_MENU, self.OnUsageGuide, id=4)
        self.Bind(adv.EVT_CALENDAR_SEL_CHANGED, self.OnDateChange)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        self.Bind(wx.EVT_BUTTON, self.OnPlot, self.plotButton)
        self.Bind(wx.EVT_BUTTON, self.OnAddToPlot, self.addPlotButton)
        # self.Bind(wx.EVT_SET_FOCUS, self.OnFocus())

    # def OnIdle(self, event):
    #     self.count = self.count + 1
    #     if self.count >= 100:
    #         self.count = 0
    #     self.gauge.SetValue(self.count)

    def OnDateChange(self, event):
        From = self.From.GetDate()
        To = self.To.GetDate()
        temp = str(self.From.GetDate()).split(' ')
        dateRange = [[int(i) for i in temp[0].split('/')]]
        temp = str(self.To.GetDate()).split(' ')
        dateRange.append([int(i) for i in temp[0].split('/')])
        if BFuns.compareDate(dateRange[0], self.values[0][0]) == 1:
            self.From.SetDate(wx.DateTime(self.values[0][0][1], self.values[0][0][0] - 1, self.values[0][0][2]))
        elif BFuns.compareDate(dateRange[0], self.values[-1][0]) == -1:
            self.From.SetDate(wx.DateTime(self.values[-1][0][1], self.values[-1][0][0] - 1, self.values[-1][0][2]))
        elif BFuns.compareDate(dateRange[1], self.values[-1][0]) == -1:
            self.To.SetDate(wx.DateTime(self.values[-1][0][1], self.values[-1][0][0] - 1, self.values[-1][0][2]))
        if To < From:
            self.To.SetDate(self.From.GetDate())

    def OnQuit(self, event):
        plt.close('all')
        self.Destroy() # When called by wx.EVT_CLOSE calling self.Close() causes infinite loop

    def OnAbout(self, event):
        wx.MessageBox("This is a App for Instrumentation Project","About Crowd Analyzer", wx.OK | wx.ICON_INFORMATION, self)

    def OnUsageGuide(self, event):
        wx.MessageBox(self.usageInfo, 'Instructions To Use', wx.OK, self)

    def OnReload(self, event):
        self.counts = self.LoadFile()
        self.ReloadStaticText()
        wx.MessageBox("Sample data updated and other information Refetched", "About Data Change", wx.OK | wx.ICON_INFORMATION, self)
    # def OnFocus(self):
    #     plt.clf()

if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()