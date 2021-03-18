import urllib.request
from html.parser import HTMLParser

#Test comment for commit to network drive remote

marketwatch_base_url = "https://www.marketwatch.com/investing/Fund/"

def GetStockPrice(ticker_name):
    request_url = marketwatch_base_url + ticker_name
    request_response = urllib.request.urlopen(request_url).read()
    request_response_text = request_response.decode("utf8")
    marketwatch_parser = MarketWatchHTMLParser()  
    marketwatch_parser.feed(request_response_text)
    ticker_value = marketwatch_parser.return_ticker_value()
    return ticker_value 
    
class MarketWatchHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.is_in_h3 = False
        self.is_ticker_value = False
        self.last_tag = None
        self.ticker_value = None
        
    
    def handle_starttag(self, tag, attrs):
        if tag == 'h3':
            self.is_in_h3 = True
        if tag == 'bg-quote':
            for name, value in attrs:
                if name == 'class' and value == 'value':
                    self.is_ticker_value = True
                    self.last_tag = 'bg-quote' 
                    
    def handle_endtag(self, tag):
        if tag == 'h3':
            self.is_in_h3 = False
        if tag == 'bg-quote':
            self.is_ticker_value = False                        
                    
    def handle_data(self, data):
        if self.last_tag == 'bg-quote' and self.is_ticker_value and self.is_in_h3:
            self.ticker_value = data
            self.return_ticker_value()
            
    def return_ticker_value(self):
        return self.ticker_value


def main():     
    ticker_input = "VOO"    
    stock_value = GetStockPrice(ticker_input)
    print(stock_value)
    
if __name__ == "__main__":
    main()
    

    