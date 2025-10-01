import mysql.connector as my
mydb= my.connect(host='localhost',user='root',database='python_bank',passwd="root")
c=mydb.cursor()
pd = input('enter your password:')
bal=0
def login():
        global pd
        n = input('Enter the name:')
        b = int(input("Enter your balance:"))
        c.execute("insert into account values('{acc_name}',{balance},'{password}','Null')".format(acc_name=n,balance=b,password=pd))
        mydb.commit()
def cb():
        global bal
        c.execute("select  balance from account where password='{password}'".format(password=pd))
        rec = c.fetchall()
        bal = rec[0][0]
        print('The current balance is :',bal,'$')
def update():
        global pd,n,c
        ch = int(input('what do you want to change ?\n1.acc_name\n2.balance\n3.password'))
        if ch == 1:
                newname=input('Enter the new name:')
                c.execute("update account set acc_name='{acc_name}' where password='{password}'".format(password=pd,acc_name=newname))
                mydb.commit()
        elif ch == 2:
                newbalance=int(input('Enter the new balance:'))
                c.execute("update account set balance='{balance} where password='{password}'".format(password=pd,balance=newbalance))
                mydb.commit()
        elif ch == 3:
                newpassword=input('Enter the new password:')
                c.execute("update account set password='{nu}' where acc_name='{r}'".format(r=n,nu=newpassword))
                mydb.commit()
        else:
                print('Invalid input')
def withdrawal():
        global bal,c,pd
        amt = int(input('Enter how much you want to withdraw from the bank:'))
        if bal-amt > 0:
                c.execute("update account set balance='{balance}' where password='{password}'".format(password=pd,balance=bal-amt))
                mydb.commit()
        else:
                print('Incorrect amount')
        cb()
def deposit():
        global bal,c,pd
        amt = int(input('Enter how much you want to deposit to the bank:'))
        c.execute("update account set balance='{balance}' where password='{password}'".format(password=pd,balance=bal+amt))
        mydb.commit()
        cb()
def transfermoney():
        global pd,c,n,bal
        c.execute("select acc_name from account where acc_name!='{acc_name}'".format(acc_name=n))
        rec=c.fetchall()
        print('\t| ACCOUNTS |')
        l=[]
        for i in rec:
                print('\t ',i[0])
                l.append(i[0])
        acc = input('Enter the account you want to transfer money into:')
        num = int(input('Enter how much money you want to transfer:'))
        if acc not in l:
                print('Invalid input')
        if num > bal:
                print('invalid input')
        c.execute("select  balance from account where acc_name='{acc_name}'".format(acc_name=acc))
        rec = c.fetchall()
        bal1 = rec[0][0]
        print(bal1)
        c.execute("update account set balance='{balance}' where acc_name='{acc_name}'".format(acc_name=acc,balance=bal1+num))
        mydb.commit()
        print('Transfer successful')
def delete():
        c.execute("Delete from account where password='{password}'".format(password=pd))
        mydb.commit()
print('1.sign  in \n2.registered already \n3.quit')
choice=input('Enter your choice:')
if choice == '2':
        c.execute("select  acc_name from account where password='{password}'".format(password=pd))
        rec=c.fetchall()
        n=rec[0][0]
elif choice == '1':
        login()
while choice not in '120':
        print('log in , quit (0/1)')
        choice=input('Enter your choice:')
print(cb())
while True:
        print('1.To update the values')
        print('2.to deposit money into the bank')
        print('3.to withdraw money from the bank')
        print('4.to transfer money to another account')
        print('5.delete')
        ch = int(input('Enter the choice(1/2/3/4/5):'))
        if ch == 1:
                update()
        elif ch==2:
                deposit()
        elif ch==3:
                withdrawal()
        elif ch==4:
                transfermoney()
        elif ch == 5:
                delete()
        else:
                print('ERROR')
                break
