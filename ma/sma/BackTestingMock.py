from ma.sma import SmaSecond as sma
import matplotlib.pyplot as plt


#           Plan
# 1. Name of the Stock
# 2. Time Period of the stock
# 3. Get the indicators
# 4. Compute Profit/Loss

def main():
    data = sma.run_sma_bot('TSLA', '2019-1-1', '2020-8-1')
    budget = 10000  # EURO
    starting_budget = budget
    profit_lst = []

    # find the first buy in place
    index_buy = 0
    for i in range(data['ACTION'].size):
        if (data['ACTION'][i] == 'BUY'):
            index_buy = i
            break

    stocks = budget / data['Close'][index_buy]  # number of stocks owned when starting
    budget = 0

    for i in range(index_buy + 1, data['ACTION'].size):
        if data['ACTION'][i] == 'SELL':
            budget = stocks * data['Close'][i]
            stocks = 0
            profit_lst.append(budget)
        elif data['ACTION'][i] == 'BUY':
            stocks = budget / data['Close'][i]

    if budget == 0:
        # MEANS THAT WE HAVE TO SELL
        budget = stocks * data['ACTION'][data['ACTION'].size - 1]

    print('BUDGET IS NOW: ' + str(budget))
    profit = ((budget - starting_budget) * 100) / starting_budget
    print('Profit is: ' + str(profit) + "%")

    plt.figure(figsize=(12, 6))
    plt.plot(profit_lst, label=' Budget', linewidth=2)
    plt.xlabel('TIME')
    plt.ylabel('Adjusted closing price ($)')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
