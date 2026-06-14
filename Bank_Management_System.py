import mysql.connector

con=None
crsr=None

con=mysql.connector.connect(
    user='root',
    password='Aparna@217',
    database='bank_db',
    host='localhost'
)

crsr=con.cursor()

# def create_account():
#     name=input("Enter Your Name : ")
#     balance=float(input("Enter Your Initial Balance : "))

#     query="""
#             CREATE TABLE ACCOUNTS(
#             ACC_NO INT PRIMARY KEY AUTO_INCREMENT,CUST_NAME VARCHAR(30),BALANCE DECIMAL(10,2))
#           """

def create_account():
    name=input("Enter Your Name : ")
    balance=float(input("Enter Your Initial Balance : "))
    
    if balance < 500:
        print("Initial Balance Must Be Minimum 500!")
        return

    query="""
            INSERT INTO ACCOUNTS
            (CUST_NAME,BALANCE)
            VALUES(%s,%s)

          """
    crsr.execute(query,(name,balance))
    con.commit()
    print("Account Created Successfully!")

def deposit():
    acc_no=int(input("Enter Your Account Number : "))
    amount=int(input("Enter Your Amount : "))

    query_check="""
            SELECT ACC_NO
            FROM ACCOUNTS
            WHERE ACC_NO = %s

          """
    crsr.execute(query_check,(acc_no,))
    res=crsr.fetchone()
    if res is None:
        print("Account Not Found!")
        return

    if amount > 0:
        query="""
                UPDATE ACCOUNTS 
                SET BALANCE=BALANCE + %s
                WHERE ACC_NO = %s

              """   
        crsr.execute(query,(amount,acc_no))
        con.commit()
        print("Amount Credited Successfully!")
    else:
        print("Enter Valid Amount!")

def withdraw():
    acc_no=int(input("Enter Your Account Number : "))
    amount=int(input("Enter Your Amount : "))

    if amount <=0:
        print("Enter Valid Amount!")
        return

    query="""
            SELECT BALANCE
            FROM ACCOUNTS
            WHERE ACC_NO = %s

          """   
    crsr.execute(query,(acc_no,))
    res=crsr.fetchone()

    if res!=None:
        balance=res[0]
        if balance>=amount:
            query="""
                    UPDATE ACCOUNTS
                    SET BALANCE=BALANCE - %s
                    WHERE ACC_NO = %s

                  """
            crsr.execute(query,(amount,acc_no))
            con.commit()
            print("Amount Debited Successfully!")
        else:
            print("Insufficient Balance!")
    else:
        print("Account Not Found!")

def check_balance():
    acc_no=int(input("Enter Your Account Number : "))

    query="""
            SELECT * 
            FROM 
            ACCOUNTS
            WHERE ACC_NO = %s

          """
    crsr.execute(query,(acc_no,))
    res=crsr.fetchone()
    con.commit()

    if res!=None:
        print("-------- Account Details --------")
        print("Account Number : ",res[0])
        print("Account Holder Name : ",res[1])
        print("Account Balance : ",res[2])
        print("----------------------------------")
    else:
        print("Account Not Found!")

def transfer_amount():
    sender=int(input("Enter Sender's Account Number : "))
    receiver=int(input("Enter Receiver's Account Number : "))
    amount=int(input("Enter Your Amount : "))

    query="""
            SELECT BALANCE
            FROM ACCOUNTS
            WHERE ACC_NO = %s

          """
    crsr.execute(query,(sender,))
    res=crsr.fetchone()

    if res!=None:
        balance=res[0]

        query_rec="""
                SELECT ACC_NO
                FROM ACCOUNTS
                WHERE ACC_NO = %s

              """
        crsr.execute(query_rec,(receiver,))
        receiver=crsr.fetchone()
        if receiver is None:
            print("Receiver Account Not Found!")
            return

        if balance >= amount:
            try:
                query1="""
                        UPDATE ACCOUNTS
                        SET BALANCE = BALANCE - %s
                        WHERE ACC_NO = %s

                       """
                crsr.execute(query1,(amount,sender))

                query2="""
                        UPDATE ACCOUNTS
                        SET BALANCE = BALANCE + %s
                        WHERE ACC_NO = %s

                       """
                crsr.execute(query2,(amount,receiver))
                con.commit()
                print("Money Transferred Successfully!")
            except Exception as e:
                con.rollback()
                print("Transaction Failed...!")
                print(e)
        else:
            print("Insufficient Balance!")
    else:
        print("Sender Account Not Found!")

def delete_account():
    acc_no=int(input("Enter Your Account Number : "))

    query="""
            DELETE FROM
            ACCOUNTS
            WHERE ACC_NO = %s

          """
    crsr.execute(query,(acc_no,))

    if crsr.rowcount > 0:
        print("Account Deleted Successfully!")
        con.commit()
    else:
        print("Account Does Not Exists!")

def view_all_accounts():
    query="""
            SELECT * FROM ACCOUNTS
          """                     
    crsr.execute(query)
    rows=crsr.fetchall()
    con.commit()

    print("<----- All Account Details ----->")
    for row in rows:
        print("\n Account Number : ",row[0])
        print("Account Holder Name : ",row[1])
        print("Account Balance : ",row[2])
        print("-------------------------------")
print("<======= WELECOME TO BANK MANAGEMENT SYSTEM =======>")

while True:
    print("1. CREATE ACCOUNT")
    print("2. DEPOSIT AMOUNT")
    print("3. WITHDRAW AMOUNT")
    print("4. CHECK BALANCE")
    print("5. TRANSFER MONEY")
    print("6. DELETE ACCOUNT")
    print("7. VIEW ALL ACCOUNTS")
    print("8. EXIT FROM THE APP")

    choice=int(input("Enter Your Choice : "))

    match choice:
        case 1: create_account()
        case 2: deposit()
        case 3: withdraw()
        case 4: check_balance()
        case 5: transfer_amount()
        case 6: delete_account()
        case 7: view_all_accounts()
        case 8: 
            print("<===== THANK YOU, VISIT AGAIN...! =====>")
            if crsr!=None:
                crsr.close()
            if con!=None:
                con.close()
            break
        case _: print("Invalid Choice, Try Again!") 

                              