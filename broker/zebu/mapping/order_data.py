import json
from database.token_db import get_symbol, get_oa_symbol 

def map_order_data(order_data):
    """
    Processes and modifies a list of order dictionaries based on specific conditions.
    
    Parameters:
    - order_data: A list of dictionaries, where each dictionary represents an order.
    
    Returns:
    - The modified order_data with updated 'tradingsymbol' and 'product' fields.
    """
        # Check if 'data' is None
    if order_data is None or (isinstance(order_data, dict) and (order_data['stat'] == "Not_Ok")):
        # Handle the case where there is no data
        # For example, you might want to display a message to the user
        # or pass an empty list or dictionary to the template.
        print("No data available.")
        order_data = {}  # or set it to an empty list if it's supposed to be a list
    else:
        order_data = order_data
        


    if order_data:
        for order in order_data:
            # Extract the instrument_token and exchange for the current order
            symboltoken = order['token']
            exchange = order['exch']
            
            # Use the get_symbol function to fetch the symbol from the database
            symbol_from_db = get_symbol(symboltoken, exchange)
            
            # Check if a symbol was found; if so, update the trading_symbol in the current order
            if symbol_from_db:
                order['tsym'] = symbol_from_db
                if (order['exch'] == 'NSE' or order['exch'] == 'BSE') and order['prd'] == 'C':
                    order['prd'] = 'CNC'
                               
                elif order['prd'] == 'I':
                    order['prd'] = 'MIS'
                
                elif order['exch'] in ['NFO', 'MCX', 'BFO', 'CDS'] and order['prd'] == 'M':
                    order['prd'] = 'NRML'

                if(order['prctyp']=="MKT"):
                    order['prctyp']="MARKET"
                elif(order['prctyp']=="LMT"):
                    order['prctyp']="LIMIT"
                elif(order['prctyp']=="SL-MKT"):
                    order['prctyp']="SL-M"
                elif(order['prctyp']=="SL-LMT"):
                    order['prctyp']="SL"
                
            else:
                print(f"Symbol not found for token {symboltoken} and exchange {exchange}. Keeping original trading symbol.")
                
    return order_data


def calculate_order_statistics(order_data):
    """
    Calculates statistics from order data, including totals for buy orders, sell orders,
    completed orders, open orders, and rejected orders.

    Parameters:
    - order_data: A list of dictionaries, where each dictionary represents an order.

    Returns:
    - A dictionary containing counts of different types of orders.
    """
    # Initialize counters
    total_buy_orders = total_sell_orders = 0
    total_completed_orders = total_open_orders = total_rejected_orders = 0

    if order_data:
        for order in order_data:
            # Count buy and sell orders
            if order['trantype'] == 'B':
                order['trantype'] = 'BUY'
                total_buy_orders += 1
            elif order['trantype'] == 'S':
                order['trantype'] = 'SELL'
                total_sell_orders += 1
            
            # Count orders based on their status
            if order['status'] == 'COMPLETE':
                total_completed_orders += 1
            elif order['status'] == 'OPEN':
                total_open_orders += 1
            elif order['status'] == 'REJECTED':
                total_rejected_orders += 1

    # Compile and return the statistics
    return {
        'total_buy_orders': total_buy_orders,
        'total_sell_orders': total_sell_orders,
        'total_completed_orders': total_completed_orders,
        'total_open_orders': total_open_orders,
        'total_rejected_orders': total_rejected_orders
    }


def transform_order_data(orders):
    

    transformed_orders = []
    
    for order in orders:
        # Make sure each item is indeed a dictionary
        if not isinstance(order, dict):
            print(f"Warning: Expected a dict, but found a {type(order)}. Skipping this item.")
            continue

        transformed_order = {
            "symbol": order.get("tsym", ""),
            "exchange": order.get("exch", ""),
            "action": order.get("trantype", ""),
            "quantity": order.get("qty", 0),
            "price": order.get("prc", 0.0),
            "trigger_price": order.get("trgprc", 0.0),
            "pricetype": order.get("prctyp", ""),
            "product": order.get("prd", ""),
            "orderid": order.get("norenordno", ""),
            "order_status": order.get("status", "").lower(),
            "timestamp": order.get("norentm", "")
        }

        transformed_orders.append(transformed_order)

    return transformed_orders



def map_trade_data(trade_data):
    """
    Processes and modifies a list of order dictionaries based on specific conditions.
    
    Parameters:
    - order_data: A list of dictionaries, where each dictionary represents an order.
    
    Returns:
    - The modified order_data with updated 'tradingsymbol' and 'product' fields.
    """
        # Check if 'data' is None
    if trade_data is None or (isinstance(trade_data, dict) and (trade_data['stat'] == "Not_Ok")):
        # Handle the case where there is no data
        # For example, you might want to display a message to the user
        # or pass an empty list or dictionary to the template.
        print("No data available.")
        trade_data = {}  # or set it to an empty list if it's supposed to be a list
    else:
        trade_data = trade_data
        


    if trade_data:
        for order in trade_data:
            # Extract the instrument_token and exchange for the current order
            symbol = order['tsym']
            exchange = order['exch']
            
            # Use the get_symbol function to fetch the symbol from the database
            symbol_from_db = get_oa_symbol(symbol, exchange)
            
            # Check if a symbol was found; if so, update the trading_symbol in the current order
            if symbol_from_db:
                order['tsym'] = symbol_from_db
                if (order['exch'] == 'NSE' or order['exch'] == 'BSE') and order['prd'] == 'C':
                    order['prd'] = 'CNC'
                               
                elif order['prd'] == 'I':
                    order['prd'] = 'MIS'
                
                elif order['exch'] in ['NFO', 'MCX', 'BFO', 'CDS'] and order['prd'] == 'M':
                    order['prd'] = 'NRML'

                if(order['trantype']=="B"):
                    order['trantype']="BUY"
                elif(order['trantype']=="S"):
                    order['trantype']="SELL"
                
                
            else:
                print(f"Unable to find the symbol {symbol} and exchange {exchange}. Keeping original trading symbol.")
                
    return trade_data




def transform_tradebook_data(tradebook_data):
    transformed_data = []
    for trade in tradebook_data:
        transformed_trade = {
            "symbol": trade.get('tsym', ''),
            "exchange": trade.get('exch', ''),
            "product": trade.get('prd', ''),
            "action": trade.get('trantype', ''),
            "quantity": trade.get('qty', 0),
            "average_price": trade.get('avgprc', 0.0),
            "trade_value": float(trade.get('avgprc', 0)) * int(trade.get('qty', 0)),
            "orderid": trade.get('norenordno', ''),
            "timestamp": trade.get('norentm', '')
        }
        transformed_data.append(transformed_trade)
    return transformed_data


def map_position_data(position_data):

    if  position_data is None or (isinstance(position_data, dict) and (position_data['stat'] == "Not_Ok")):
        # Handle the case where there is no data
        # For example, you might want to display a message to the user
        # or pass an empty list or dictionary to the template.
        print("No data available.")
        position_data = {}  # or set it to an empty list if it's supposed to be a list
    else:
        position_data = position_data
        


    if position_data:
        for order in position_data:
            # Extract the instrument_token and exchange for the current order
            symbol = order['tsym']
            exchange = order['exch']
            
            # Use the get_symbol function to fetch the symbol from the database
            symbol_from_db = get_oa_symbol(symbol, exchange)
            
            # Check if a symbol was found; if so, update the trading_symbol in the current order
            if symbol_from_db:
                order['tsym'] = symbol_from_db
                if (order['exch'] == 'NSE' or order['exch'] == 'BSE') and order['prd'] == 'C':
                    order['prd'] = 'CNC'
                               
                elif order['prd'] == 'I':
                    order['prd'] = 'MIS'
                
                elif order['exch'] in ['NFO', 'MCX', 'BFO', 'CDS'] and order['prd'] == 'M':
                    order['prd'] = 'NRML'


                
                
            else:
                print(f"Unable to find the symbol {symbol} and exchange {exchange}. Keeping original trading symbol.")
                
    return position_data


def transform_positions_data(positions_data):
    transformed_data = []
    for position in positions_data:
        transformed_position = {
            "symbol": position.get('tsym', ''),
            "exchange": position.get('exch', ''),
            "product": position.get('prd', ''),
            "quantity": position.get('netqty', 0),
            "average_price": position.get('netavgprc', 0.0),
        }
        transformed_data.append(transformed_position)
    return transformed_data



def map_portfolio_data(portfolio_data):
    """
    Processes and modifies a list of Portfolio dictionaries based on specific conditions and
    ensures both holdings and totalholding parts are transmitted in a single response.
    
    Parameters:
    - portfolio_data: A dictionary, where keys are 'holdings' and 'totalholding',
                      and values are lists/dictionaries representing the portfolio information.
    
    Returns:
    - The modified portfolio_data with 'product' fields changed for 'holdings' and 'totalholding' included.
    """
    # Check if 'data' is None or doesn't contain 'holdings'
    if not portfolio_data:
        print("No data available.")
        # Return an empty structure or handle this scenario as needed
        return {}

    # Directly work with 'data' for clarity and simplicity
    portfolio_data = portfolio_data

    # Modify 'product' field for each holding if applicable
    for portfolio in portfolio_data:
        exch_tsym_list = portfolio.get('exch_tsym', [])
        
        # Process each symbol in the 'exch_tsym' list
        for exch_tsym in exch_tsym_list:
            symbol = exch_tsym.get('tsym', '')
            exchange = exch_tsym.get('exch', '')

            # Replace 'get_oa_symbol' function with your actual symbol fetching logic
            symbol_from_db = get_oa_symbol(symbol, exchange)
            
            # Check if a symbol was found; if so, update the trading symbol in the current holding
            if symbol_from_db:
                exch_tsym['tsym'] = symbol_from_db
            else:
                print(f"Zebu Portfolio - Product Value for {symbol} Not Found or Changed.")
    
    # Directly returning the modified portfolio data
    return portfolio_data
    



def calculate_portfolio_statistics(holdings_data):
    
    totalholdingvalue = 0
    totalinvvalue = 0
    totalprofitandloss = 0
    totalpnlpercentage = 0

    

    if holdings_data is None or (isinstance(holdings_data, dict) and (holdings_data['stat'] == "Not_Ok")):
        print("No data available.")
        
    return {
        'totalholdingvalue': totalholdingvalue,
        'totalinvvalue': totalinvvalue,
        'totalprofitandloss': totalprofitandloss,
        'totalpnlpercentage': totalpnlpercentage
    }


def transform_holdings_data(holdings_data):
    transformed_data = []
    if(isinstance(holdings_data, list)):
        for holdings in holdings_data[0]['exch_tsym']:
            transformed_position = {
                "symbol": holdings.get('tsym', ''),
                "exchange": holdings.get('exch', ''),
                "quantity": holdings.get('quantity', 0),
                "product": holdings.get('product', ''),
                "pnl": holdings.get('profitandloss', 0.0),
                "pnlpercent": holdings.get('pnlpercentage', 0.0)
            }
            transformed_data.append(transformed_position)
    return transformed_data