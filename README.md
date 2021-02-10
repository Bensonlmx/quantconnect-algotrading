#### Strategy Introduction

The aim of this exercise to present a strategy to achieve moderate returns using a balanced portfolio of assets. For this purpose, we have allocated capital in the following asset classes identified at the specified percentages 
1.	40% of capital - Top performing REIT Stocks from the S & P (“SPY”) index
2.	45% of capital - Vanguard FTSE Developed Markets ETF (“VEA”)
3.	15% of capital - SPDR Gold Trust (“GLD”)
The reasons for selecting REIT, ETFs and Gold are for diversification and for their inherent qualities of having a consistent rising momentum throughout the decade and stable growth over longer period of time.  In addition, the REIT asset class distributes their profits as dividends which could be an uplift to the capital invested.  In short, we believe that the above allocation optimizes the returns for the investors over a longer time period.  The CAGR is expected to be ~4% over 10 year period.  The important point to note is, the portfolio has performed through the Global, financial crisis, US debt crisis, European debt crisis, Fukushima meltdown and the latest COV-ID pandemic. 

### Portfolio Performance – Period Jan 2011- Jan 2021

![performance] (https://github.com/Bensonlmx/quantconnect-algotrading/blob/master/performance.png)

#### Methods

As indicated, the assets in the portfolio were identified to provide stable returns.  To fine tune the returns, the momentum strategy is adopted.  This momentum strategy assumes that the asset which grows strongly in the past will continue to grow in the near future too.  This strategy captures the rate of change over a period of 11 months and reallocates the portfolio to provide stable returns on quarterly basis.  The following trading confirmations are made in the algorithm to safeguard investor’s interest

1.	Quarterly Portfolio reallocation will not happen if the total portfolio value is less than the invested value (e.g. US$ 100,000 in our case). 
2.	Algorithm cross checks the month and allocates only every quarter.
3.	The component companies of the REIT asset portfolio will be liquidated and reallocated every quarter.  The Algorithm selects top 5-10 companies in the S & P REIT portfolio and allocates the capital in them accordingly.  If the REIT stock is not in top 5 selection criteria, that particular REIT stock will be dropped for that quarter during asset re allocation.

The algorithm selects the REIT stocks on the basis of coarse and fine universe selection. In this an investment universe of coarse stocks pack that have prices greater than US$, contains fundamental data and have a trading volume more than 1,000,000 is created and then from this coarse stocks pack, the algorithm filters out the REIT only stocks using the Morningstar field “IsREIT” property.

From the fine-tuned stock pack, the algorithm calculates each REIT’s 11 month return one month lagged and rank them in the ascending order.  Once ranked bottom to top, the algorithm picks up the top 5-10 performing stocks from the fine-tuned list and invests accordingly.
