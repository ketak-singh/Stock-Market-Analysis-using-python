# Stock-Market-Analysis-using-python

## The aim of this project was to write a python code that with the help of an Application Program Interface can fetch the entire data present on the website for a particular symbol / keyword passed in as input.

### The python code takes in a symbol as an input. These symbols are the symbols assigned to world wide companies. Every company has it's own symbol.
For example recently with the name change of the company "Facebook" to "Meta" their company's symbol was also chnaged from 'FB' to 'META'

### The input symbol is taken in and passed into the API url which brings in all the data present on the website for that particular symbol.

### The API used is from the website : https://www.yahoofinanceapi.com/

### There are multiple APIs that can be used based on what kind of data has to be procured or fetched. 

### In this project we have just used two of the many APIs presnt in the above given website. 

### The APIs used are 
1) GET /v6/finance/quote
2) GET/v7/finance/options/{symbol}

The first one being used to get the Real time quote data for stocks, ETFs, mutuals funds, etc. 

The second one used for getting the option chain for a particular symbol

Both these data are recived as a JSON file. So the next task of the python code is to convert the JSON file to a pandas dataframe and also a CSV file.

But before the conversion the data needs to be processed and only the data which is needed was extracted through python code.


### The final outputs are stored as two CSV files