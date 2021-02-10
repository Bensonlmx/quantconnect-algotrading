class VentralVerticalCircuit(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2011,1,1) #Set  Start date
        self.SetEndDate(2021,1,1)  #Set end date  
        self.SetCash(100000)  # Set Strategy Cash
        
        #selecting top performing REIT's using coarse and fine selection logic
        self.UniverseSettings.Resolution = Resolution.Daily
        self.filtered_fine = None
        self.AddUniverse(self.CoarseSelectionFunction,self.FineSelectionFunction)
        self.AddEquity("SPY", Resolution.Daily)
        self.AddEquity("VEA", Resolution.Daily) # Vanguard FTSE Developed Markets ETF
        self.AddEquity("GLD", Resolution.Daily) # SPDR Gold Trust
        #self.AddEquity("TLT", Resolution.Daily) # iShares 20+ Year Treasury Bond ETF
        # self.AddCrypto("BTCUSD", Resolution.Daily) # Bitcoin
        #self.AddEquity("GLD", Resolution.Daily) # SPDR Gold Trust
        #monthly scheduled event
        self.Schedule.On(self.DateRules.MonthStart("SPY"), self.TimeRules.At(23, 0), self.rebalance)
        self.months = -1
        self.quarterly_rebalance = False
        self.acc_returns = 0
        
    def CoarseSelectionFunction(self, coarse):
        if self.quarterly_rebalance:
            # drops penny stocks, stocks that have more than 10000 Volume and stocks with no fundamental data
            self.filtered_coarse = [x.Symbol for x in coarse if (float(x.Price) > 1)
                                                            and (x.HasFundamentalData)
                                                            and float(x.Volume) > 1000000]    
            return self.filtered_coarse
        else: 
            return []      
    
    def FineSelectionFunction(self, fine):
        if self.quarterly_rebalance:
            #filters out the companies that are not REITs
            fine = [x for x in fine if (x.CompanyReference.IsREIT == 1)] 
            
            #calculating the momentum using 6 month (1-day lagged) returns 
            start = self.Time-timedelta(days = 360)
            end = self.Time-timedelta(days = 30)
            for x in fine:
                hist = self.History([x.Symbol],start,end,Resolution.Daily)
                if not hist.empty:
                    start_price = hist["close"].iloc[0]
                    end_price = hist["close"].iloc[-1]
                    x.momentum = (end_price-start_price)/start_price
            
            fine = [x for x in fine if hasattr(x, 'momentum')] #hasattr returns true if certain attributes are present
            #we sort REITs based on their returns
            sorted_filter = sorted(fine, key=lambda x: x.momentum)
            self.filtered_fine = [i.Symbol for i in sorted_filter]
            return self.filtered_fine
        else:
            return []
    
    def rebalance(self):
        #halfyearly rebalance
        self.months+=1
        if self.months%3 == 0:
            self.quarterly_rebalance = True
            self.Debug("in Rebalance month" + str(self.months))
 
    def OnData(self, data):
         pvalue = self.Portfolio.TotalPortfolioValue
        self.Debug("Portfolio size is US$"  + str(pvalue))
        if not self.quarterly_rebalance: return
        self.SetHoldings("VEA", 0.45) #allocate 45% to ETF
        # self.SetHoldings("TLT", 0.15) #allocate 25% to bond
        self.SetHoldings("GLD", 0.15) #allocate 15% to gold
        # self.SetHoldings("BTCUSD", 0.05) #allocate 5% to crypto
        if self.Portfolio.TotalPortfolioValue < 100000: 
            self.Debug("Portfolio size is less than 100000...Status quo" + str(pvalue))
            return
        if self.filtered_fine:  # allocating 40% to REIT stocks which has good momenetum in the previous six months
            self.Debug( "in the ondata module" + str(self.months))
            portfolio_size = int(len(self.filtered_fine)/6)
            self.Debug("Portfoliosize " + str(portfolio_size))
            #selecting top 10-15 stocks in the portfolioc, sorted list is in ascending order,that is the reason we used -portfolio size:   
            long_stocks = self.filtered_fine[-portfolio_size:]
            stocks_invested = [x.Key for x in self.Portfolio]
            for i in stocks_invested:
                #liquidate the stocks not in our filtered_fine list
                if i not in long_stocks:
                    self.Liquidate(i)
                    self.Debug("Liquidating+"+ str(i))
                elif i in long_stocks:
                    self.SetHoldings(i, (0.4/(portfolio_size)))
                    self.Debug("reallocating portfolio")
            self.quarterly_rebalance = False
            self.filtered_fine = None
