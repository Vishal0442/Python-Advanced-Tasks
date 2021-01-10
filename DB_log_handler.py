
import logging
import pymysql
import time

# collecting MySQL connection credentials
user = input("Enter MySQL user name : ",)
password = input("Enter MySQL user password : ",)
db_name = input("Enter MySQL database name : ",)


# getting MySQL connection
def get_connection():
    try:
        conn = pymysql.connect('localhost', user, password, db_name)
        return conn
    except BaseException as e:
        print(e.args)


# Function for closing DB resources
def close_resources(conn, cursor):

    try:
        if cursor:
            cursor.close()
    except BaseException as e1:
        print(e1.args)

    try:
        if conn:
            conn.close()
    except BaseException as e2:
        print(e2.args)


# Generator to generate log ID's
def myGen():
    cnt=100
    while True:
        cnt = cnt+1
        yield cnt

gen = myGen()


# Custom DB_Handler
class myDBHandler(logging.Handler):

    def emit(self, record):
        log_id = next(gen)
        #user_name = record.name
        user_name = record.name
        log_time = record.asctime
        log_level = record.levelname
        line_no = record.lineno
        fun_name = record.funcName
        log_msg = record.message

        sql = "insert into log_table values ({}, '{}', '{}', '{}', {}, '{}', '{}')".format(log_id, user_name, log_time, log_level, line_no, fun_name, log_msg)

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            close_resources(conn, cursor)

        except BaseException as e:
            print(e.args)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)
consoleHandler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(funcName)s - %(message)s"))

dbHandler = myDBHandler()
dbHandler.setLevel(logging.INFO)
dbHandler.setFormatter(logging.Formatter("%(name)s - %(asctime)s - %(levelname)s - %(lineno)d - %(funcName)s - %(message)s"))

logger.addHandler(consoleHandler)
logger.addHandler(dbHandler)


def function_one():
    for i in range(1000):
        logger.debug("This is logging DEBUG msg --> 10")
        logger.info("This is logging INFO msg --> 20")
        logger.warning("This is logging WARNING msg --> 30")
        logger.error("This is logging ERROR msg --> 40")
        logger.critical("This is logging CRITICAL msg --> 50")
        logger.info("Iteration number : " + str(i))
        time.sleep(5)

if __name__ == "__main__":
    function_one()


