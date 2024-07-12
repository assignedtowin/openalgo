import json
from database.token_db import get_symbol , get_oa_symbol

def map_order_data(order_data):
    """
    Processes and modifies a list of order dictionaries based on specific conditions.
    
    Parameters:
    - order_data: A list of dictionaries, where each dictionary represents an order.
    
    Returns:
    - The modified order_data with updated 'tradingsymbol' and 'product' fields.
    """
    if isinstance(order_data, dict):
        if order_data['stat'] == 'Not_Ok' :
            # Handle the case where there is an error in the data
            # For example, you might want to display an error message to the user
            # or pass an empty list or dictionary to the template.
            print(f"Error fetching order data: {order_data['emsg']}")
            order_data = {}
    else:
        order_data = order_data
        
    # print(order_data)

    if order_data:
        for order in order_data:
            # Extract the instrument_token and exchange for the current order
            exchange = order['Exchange']
            symbol = order['Trsym']
       
            
            # Check if a symbol was found; if so, update the trading_symbol in the current order
            if symbol:
                order['Trsym'] = get_oa_symbol(symbol=symbol,exchange=exchange)
            else:
                print(f"{symbol} and exchange {exchange} not found. Keeping original trading symbol.")
                
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
            if order['Trantype'] == 'B':
                total_buy_orders += 1
            elif order['Trantype'] == 'S':
                total_sell_orders += 1
            
            # Count orders based on their status
            if order['Status'] == 'complete':
                total_completed_orders += 1
            elif order['Status'] == 'open':
                total_open_orders += 1
            elif order['Status'] == 'rejected':
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
    # Directly handling a dictionary assuming it's the structure we expect
    if isinstance(orders, dict):
        # Convert the single dictionary into a list of one dictionary
        orders = [orders]

    transformed_orders = []
    print(orders)
    for order in orders:
        # Make sure each item is indeed a dictionary
        if not isinstance(order, dict):
            print(f"Warning: Expected a dict, but found a {type(order)}. Skipping this item.")
            continue
        
        # Check if the necessary keys exist in the order
        if 'Trantype' not in order or 'Prctype' not in order:
            print("Error: Missing required keys in the order. Skipping this item.")
            continue
        
        if order['Trantype'] == 'B':
            trans_type = 'BUY'
        elif order['Trantype'] == 'S':
            trans_type = 'SELL'
        else:
            trans_type = 'UNKNOWN'

        if order['Prctype'] == 'MKT':
            order_type = 'MARKET'
        elif order['Prctype'] == 'L':
            order_type = 'LIMIT'
        elif order['Prctype'] == 'SL':
            order_type = 'SL'
        elif order['Prctype'] == 'SL-M':
            order_type = 'SL-M'
        else:
            order_type = 'UNKNOWN'

        transformed_order = {
            "symbol": order.get("Trsym", ""),
            "exchange": order.get("Exchange", ""),
            "action": trans_type,
            "quantity": order.get("Qty", 0),
            "price": order.get("Prc", 0.0),
            "trigger_price": order.get("Trgprc", 0.0),
            "pricetype": order_type,
            "product": order.get("Pcode", ""),
            "orderid": order.get("Nstordno", ""),
            "order_status": order.get("Status", ""),
            "timestamp": order.get("orderentrytime", "")
        }

        transformed_orders.append(transformed_order)

    return transformed_orders


def map_trade_data(trade_data):
    return map_order_data(trade_data)

def transform_tradebook_data(tradebook_data):
    transformed_data = []
    for trade in tradebook_data:
     
        transformed_trade = {
            "symbol": trade.get('tradingsymbol'),
            "exchange": trade.get('exchange', ''),
            "product": trade.get('product', ''),
            "action": trade.get('transaction_type', ''),
            "quantity": trade.get('quantity', 0),
            "average_price": trade.get('average_price', 0.0),
            "trade_value": trade.get('quantity', 0) * trade.get('average_price', 0.0),
            "orderid": trade.get('order_id', ''),
            "timestamp": trade.get('order_timestamp', '')
        }
        transformed_data.append(transformed_trade)
    return transformed_data

def map_position_data(position_data):
    """
    Processes and modifies a list of OpenPosition dictionaries based on specific conditions.
    
    Parameters:
    - position_data: A list of dictionaries, where each dictionary represents an Open Position.
    
    Returns:
    - The modified order_data with updated 'tradingsymbol'
    """
        # Check if 'data' is None
    if position_data['data']['net'] is None:
        # Handle the case where there is no data
        # For example, you might want to display a message to the user
        # or pass an empty list or dictionary to the template.
        print("No data available.")
        position_data = {}  # or set it to an empty list if it's supposed to be a list
    else:
        position_data = position_data['data']['net']
        
    #print(order_data)

    if position_data:
        for position in position_data:
            # Extract the instrument_token and exchange for the current order
            exchange = position['exchange']
            symbol = position['tradingsymbol']
       
            
            # Check if a symbol was found; if so, update the trading_symbol in the current order
            if symbol:
                position['tradingsymbol'] = get_oa_symbol(symbol=symbol,exchange=exchange)
            else:
                print(f"{symbol} and exchange {exchange} not found. Keeping original trading symbol.")
                
    return position_data
    

def transform_positions_data(positions_data):
    transformed_data = [] 

    for position in positions_data:
        # Ensure average_price is treated as a float, then format to a string with 2 decimal places
        average_price_formatted = "{:.2f}".format(float(position.get('average_price', 0.0)))

        transformed_position = {
            "symbol": position.get('tradingsymbol', ''),
            "exchange": position.get('exchange', ''),
            "product": position.get('product', ''),
            "quantity": position.get('quantity', '0'),
            "average_price": average_price_formatted,
        }
        transformed_data.append(transformed_position)
    return transformed_data

def transform_holdings_data(holdings_data):
    transformed_data = []
    for holdings in holdings_data:
        transformed_position = {
            "symbol": holdings.get('tradingsymbol', ''),
            "exchange": holdings.get('exchange', ''),
            "quantity": holdings.get('quantity', 0),
            "product": holdings.get('product', ''),
            "pnl": round(holdings.get('pnl', 0.0), 2),  # Rounded to two decimals
            "pnlpercent": round((holdings.get('last_price', 0) - holdings.get('average_price', 0.0)) / holdings.get('average_price', 0.0) * 100, 2)  # Rounded to two decimals
        
        }
        transformed_data.append(transformed_position)
    return transformed_data

    
def map_portfolio_data(portfolio_data):
    """
    Processes and modifies a list of Portfolio dictionaries based on specific conditions.
    
    Parameters:
    - portfolio_data: A list of dictionaries, where each dictionary represents an portfolio information.
    
    Returns:
    - The modified portfolio_data with  'product' fields.
    """
        # Check if 'data' is None
    if portfolio_data['data'] is None:
        # Handle the case where there is no data
        # For example, you might want to display a message to the user
        # or pass an empty list or dictionary to the template.
        print("No data available.")
        portfolio_data = {}  # or set it to an empty list if it's supposed to be a list
    else:
        portfolio_data = portfolio_data['data']
        


    if portfolio_data:
        for portfolio in portfolio_data:
            if portfolio['product'] == 'CNC':
                portfolio['product'] = 'CNC'

            else:
                print(f"Zerodha Portfolio - Product Value for Delivery Not Found or Changed.")
                
    return portfolio_data


def calculate_portfolio_statistics(holdings_data):
    totalholdingvalue = sum(item['last_price'] * item['quantity'] for item in holdings_data)
    totalinvvalue = sum(item['average_price'] * item['quantity'] for item in holdings_data)
    totalprofitandloss = sum(item['pnl'] for item in holdings_data)
    
    # To avoid division by zero in the case when total_investment_value is 0
    totalpnlpercentage = (totalprofitandloss / totalinvvalue * 100) if totalinvvalue else 0

    return {
        'totalholdingvalue': totalholdingvalue,
        'totalinvvalue': totalinvvalue,
        'totalprofitandloss': totalprofitandloss,
        'totalpnlpercentage': totalpnlpercentage
    }


