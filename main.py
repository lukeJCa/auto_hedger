#!/usr/bin/env python
# coding: utf-8

# ## Peak Hedging
# This mini-project attempts to generate the optimal risk tolerant portfolio
#   based on historical trends.

# INPUT: A csv list of ticker symbols you are concerned with. Candidate lists are provided
# OUTPUT: A csv list of the most historically sound investments.

import csv
import pandas_datareader as reader
import datetime
import numpy as np

from datetime import timedelta
from bs4 import BeautifulSoup
from time import sleep

TICKER_LIST_NAME = 'S&P500.csv'
DAYS_BACK = 129


class HedgeMyShitUp():
    def __init__(self, ticker_list_name, days):
        self.ticker_list = self.read_tickers(ticker_list_name)
        self.checkpoint = 0

    # Load in the csv file containing ticker from the data file and return the list
    def read_tickers(self,ticker_list_name):
        ticker_list = []
        with open("data/" + ticker_list_name) as csvfile:
            for row in csvfile:
                ticker_list.append(str(row.strip()))
        return ticker_list

    # Get the mean and standard deviation of all % increases in stock price
    def get_statistics(self, time = 129):

        statistics_list = []
        while self.checkpoint < len(self.ticker_list):
            ticker = self.ticker_list[self.checkpoint]
            self.checkpoint += 1
            print("Currently fetching: " + ticker)
            try:
                data = reader.get_data_yahoo(symbols=ticker, start=datetime.datetime.now() - timedelta(days=time), end=datetime.datetime.now())
            except:
                data = []

            change_array = []
            for index in range(len(data) - 1):
                value_today = data.iloc[index]['Close']
                value_tmr = data.iloc[index + 1]['Close']
                change_array.append(-100+(value_tmr/value_today)*100)
            
            statistics_list.append((ticker,np.mean(change_array),np.std(change_array)))
        return statistics_list

    # Get two lists of stocks ranked by their average increase of price and std respectively
    def get_ranked_lists(self,ordered_list):

        mean_sorted = sorted(ordered_list, key=lambda tup: tup[1], reverse = True)
        std_sorted = sorted(ordered_list, key=lambda tup: tup[2])
        return mean_sorted,std_sorted
    
    # Find the best performing stocks as a combination of their rank in both lists.
    def combine_ranked_lists(self,list_1,list_2):

        average_score_list = []
        for ticker in self.ticker_list:
            score = 0
            for count in range(min(len(list_1),len(list_2))):
                if list_1[count][0] == ticker:
                    score += count
                if list_2[count][0] == ticker:
                    score += count
            average_score_list.append((ticker,score))

        score_sorted = sorted(average_score_list, key=lambda tup: tup[1])
        optimal_ticker_list = [seq[0] for seq in score_sorted[:50]]
        return optimal_ticker_list


# Separated due to length of the scraping operation
if __name__ == "__main__":
    hedger_object = HedgeMyShitUp(TICKER_LIST_NAME, DAYS_BACK)
    stats_list = hedger_object.get_statistics()
    mean,std = hedger_object.get_ranked_lists(stats_list)
    optimal_list = hedger_object.combine_ranked_lists(mean,std)
    print(optimal_list[:20])
    


