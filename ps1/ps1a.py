# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 06:56:12 2019

@author: mxayl
"""

# user input of starting salary
starting_salary = float(input("Enter your starting salary: "))

# assumptions
semi_annual_raise = 0.07 # every 6 months
annual_r = 0.04
portion_dp = 0.25
house = 1000000

downpayment = house * portion_dp
monthly_r = annual_r/12

savings = 0
epsilon = 100
initial_high = 10000
high = initial_high
low = 0
savings_rate_guess = ((high+low)/2)
i_guesses = 0

while abs(savings - downpayment) > epsilon: 
    i_guesses += 1
    salary = starting_salary
    savings = 0.0
    savings_rate =  savings_rate_guess / 10000
    for month in range(1, 37):
        savings += (savings*monthly_r) + ((salary/12) * savings_rate)
        if month % 6 == 0:
            salary += (salary * semi_annual_raise)
    print(i_guesses, "rate =", savings_rate_guess, "at", savings)
    prev_savings_rate = savings_rate_guess
    if savings > downpayment:
        high = savings_rate_guess
    else:
        low = savings_rate_guess
    savings_rate_guess = int(round((high+low)/2))
    if prev_savings_rate == savings_rate_guess:
        break
    
if prev_savings_rate == savings_rate_guess and savings_rate_guess == initial_high:
    print("It is not possible to pay the downpayment in three years.")
else:
    print("Best savings rate:", savings_rate)
    print("Steps in bisection search:", i_guesses)


#while current_savings < downpayment:
#    current_savings += (current_savings*monthly_r) + ((annual_salary/12)*portion_saved) 
#    months += 1
#    if months % 6 == 0:
#        annual_salary += annual_salary*semi_annual_raise
#        
#print("Number of months:", months)
    