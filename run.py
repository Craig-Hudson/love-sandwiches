import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data ():
    """
    get sales figures from user input
    """
    while True:
        print('please enter sales data from the last market')
        print('Data should be six numbers seperated by commas')
        print('Example: 10,20,30,40,50,60\n')

        data_str = input('Enter your data here: ')
        
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print('valid data')
            break
    return sales_data


def validate_data(values):
    """
    inside the try, converts all strings into ints,
    raises valueError if cannot convert string to int
    or if there isn't exactly 6 values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
        f"Exactly 6 values are required, you provided {len(values)}")
    except ValueError as e:
        print(f"Invalid data, {e}, please try again\n")
        return False

    return True

    print(values)

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock, and calculate surplus for each type

    The surplus is defined as the sales figure subtracted by the stock
    Positive indicates waste
    Negative indicates more sandwiches made on the day
    """
    print("Calculating surplus data.. \n")
    stock = SHEET.worksheet("stock").get_all_values()
    
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data


def update_worksheets(data, worksheet):
    """
    Receives a list of intergers to be inserted into a worksheet
    update the relevant worksheet with the data provided
    """
    print(f"updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully")

def get_last_five_entry_sales():
    """
    Collects columns of data from the sales worksheet collecting
    the last five entries for each sandwhich and returns the data
    as a list of lists
    """
    sales = SHEET.worksheet("sales")
    

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns

def main():
    """
    run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheets(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheets(new_surplus_data, "surplus")
    


print("Welcome to love sandwiches")
# main()
sales_columns = get_last_five_entry_sales()