'''
Please note:

The first file that you should run in this level is tests.py for database creation, with all tests passing.
Remember that running the hack.py will change the state of the database, causing some tests inside tests.py
to fail.

If you like to return to the initial state of the database, please delete the database (level-4.db) and run 
the tests.py again to recreate it.
'''

import sqlite3
import os
from flask import Flask, request

### Unrelated to the exercise -- Starts here -- Please ignore
app = Flask(__name__)
@app.route("/")
def source():
    DB_CRUD_ops().get_stock_info(request.args["input"])
    DB_CRUD_ops().get_stock_price(request.args["input"])
    DB_CRUD_ops().update_stock_price(request.args["input"])
    DB_CRUD_ops().exec_multi_query(request.args["input"])
    DB_CRUD_ops().exec_user_script(request.args["input"])
### Unrelated to the exercise -- Ends here -- Please ignore

class Connect(object):

    # helper function creating database with the connection
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
        except sqlite3.Error as e:
            print(f"ERROR: {e}")
        return connection

class Create(object):

    def __init__(self):
        con = Connect()
        try:
            # creates a dummy database inside the folder of this challenge
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            # checks if tables already exist, which will happen when re-running code
            table_fetch = cur.execute(
                '''
                SELECT name 
                FROM sqlite_master 
                WHERE type='table'AND name='stocks';
                ''').fetchall()

            # if tables do not exist, create them and insert dummy data
            if table_fetch == []:
                cur.execute(
                    '''
                    CREATE TABLE stocks
                    (date text, symbol text, price real)
                    ''')

                # inserts dummy data to the 'stocks' table, representing average price on date
                cur.execute(
                    "INSERT INTO stocks VALUES ('2022-01-06', 'MSFT', 300.00)")
                db_con.commit()

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            db_con.close()

class DB_CRUD_ops(object):

    # retrieves all info about a stock symbol from the stocks table
    # Example: get_stock_info('MSFT') will result into executing
    # SELECT * FROM stocks WHERE symbol = 'MSFT'
    def get_stock_info(self, stock_symbol):
        # building database from scratch as it is more suitable for the purpose of the lab
        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            res = "[METHOD EXECUTED] get_stock_info\n"

            # a block list (aka restricted characters) that should not exist in user-supplied input
            restricted_chars = ";%&^!#-"
            # checks if input contains characters from the block list
            has_restricted_char = any([char in stock_symbol for char in restricted_chars])
            # checks if input contains single quotes which could indicate SQL injection
            has_injection_chars = "'" in stock_symbol

            # performs the checks for good cyber security and safe software against SQL injection
            if has_restricted_char or has_injection_chars:
                res += "CONFIRM THAT THE INPUT IS NOT MALICIOUS TO EXECUTE"
            else:
                # use parameterized query to prevent SQL injection
                cur.execute("SELECT * FROM stocks WHERE symbol = ?", (stock_symbol,))

                query_outcome = cur.fetchall()
                for result in query_outcome:
                    res += "[RESULT] " + str(result)
            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            db_con.close()

    # retrieves the price of a stock symbol from the stocks table
    # Example: get_stock_price('MSFT') will result into executing
    # SELECT price FROM stocks WHERE symbol = 'MSFT'
    def get_stock_price(self, stock_symbol):
        # building database from scratch as it is more suitable for the purpose of the lab
        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            res = "[METHOD EXECUTED] get_stock_price\n"
            # use parameterized query to prevent SQL injection
            cur.execute("SELECT price FROM stocks WHERE symbol = ?", (stock_symbol,))
            query_outcome = cur.fetchall()
            for result in query_outcome:
                res += "[RESULT] " + str(result) + "\n"
            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            db_con.close()

    # updates stock price
    def update_stock_price(self, stock_symbol, price):
        # building database from scratch as it is more suitable for the purpose of the lab
        db = Create()
        con = Connect()
        try:
            path = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(path, 'level-4.db')
            db_con = con.create_connection(db_path)
            cur = db_con.cursor()

            if not isinstance(price, float):
                raise Exception("ERROR: stock price provided is not a float")

            res = "[METHOD EXECUTED] update_stock_price\n"

            # use parameterized query to prevent SQL injection
            cur.execute("UPDATE stocks SET price = ? WHERE symbol = ?", (price, stock_symbol))
            db_con.commit()
            query_outcome = cur.fetchall()
            for result in query_outcome:
                res += "[RESULT] " + result
            return res

        except sqlite3.Error as e:
            print(f"ERROR: {e}")

        finally:
            db_con.close()

    # executes multiple queries
    # Example: SELECT price FROM stocks WHERE symbol = 'MSFT';
    #          SELECT * FROM stocks WHERE symbol = 'MSFT'
    # Example: UPDATE stocks SET price = 310.0 WHERE symbol = 'MSFT'
    def exec_multi_query(self, query):
        raise Exception("ERROR: This method is not supported for security reasons")

    # executes any query or multiple queries as defined from the user in the form of script
    # Example: SELECT price FROM stocks WHERE symbol = 'MSFT';
    #          SELECT * FROM stocks WHERE symbol = 'MSFT'
    def exec_user_script(self, query):
        raise Exception("ERROR: This method is not supported for security reasons")