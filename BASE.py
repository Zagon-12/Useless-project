import mysql.connector as my
import random as r
from datetime import datetime, timedelta

mydb = my.connect(host='localhost', user='root', database='python_bank', passwd="root")
c = mydb.cursor()
bal = 0
pd = ''
no = 0
acc_type = ''  # To track account type: 'current' or 'savings'

def acc_no():
    global pd, acc_type
    if acc_type == 'current':
        c.execute("SELECT acc_no FROM account WHERE password=%s", (pd,))
    else:
        c.execute("SELECT acc_no FROM savings_account WHERE password=%s", (pd,))
    rec = c.fetchall()
    if rec:
        no = rec[0][0]
        return no
    return None

def login():
    global pd, acc_type
    acc_type = input('Enter account type (current/savings): ').lower()
    pd = input('Enter your password (Must contain at least 8 alphanumeric characters)\n:- ')
    n = input('Enter the name: ')
    b = float(input("Enter your initial balance: "))
    
    if acc_type == 'savings':
        interest = float(input("Enter annual interest rate (%): "))
        duration = int(input("Enter duration in months: "))
    
    x = ''.join(str(r.randint(0, 9)) for _ in range(8))
    
    if len(pd) >= 8 and pd.isalnum():
        if acc_type == 'current':
            c.execute("INSERT INTO account VALUES (%s, %s, %s, %s)", (n, b, pd, int(x)))
        else:
            start_date = datetime.now().date()
            c.execute("INSERT INTO savings_account VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                     (n, b, pd, interest, duration, start_date, int(x)))
        mydb.commit()
        print(f'{acc_type.capitalize()} account created successfully with account number: {x}')
    else:
        print('Password is too WEAK')

def calculate_interest():
    """Calculate and display interest for savings account"""
    global pd
    c.execute("SELECT balance, interest_rate, duration_months, start_date FROM savings_account WHERE password=%s", (pd,))
    rec = c.fetchall()
    if rec:
        balance, interest_rate, duration, start_date = rec[0]
        # Calculate interest (simple interest for demonstration)
        interest = balance * (interest_rate / 100) * (duration / 12)
        maturity_amount = balance + interest
        
        print(f"\n--- Savings Account Details ---")
        print(f"Principal Amount: ${balance:.2f}")
        print(f"Annual Interest Rate: {interest_rate}%")
        print(f"Duration: {duration} months")
        print(f"Start Date: {start_date}")
        print(f"Interest Earned: ${interest:.2f}")
        print(f"Maturity Amount: ${maturity_amount:.2f}")
        return maturity_amount
    return None

def cb():
    global bal, pd, acc_type
    if acc_type == 'current':
        c.execute("SELECT balance FROM account WHERE password=%s", (pd,))
    else:
        c.execute("SELECT balance FROM savings_account WHERE password=%s", (pd,))
    rec = c.fetchall()
    if rec:
        bal = rec[0][0]
        account_type_display = "current" if acc_type == 'current' else "savings"
        print(f'You have currently: ${bal:.2f} in your {account_type_display} bank account')
        
        if acc_type == 'savings':
            calculate_interest()

def update():
    global pd, acc_type
    print()
    if acc_type == 'current':
        ch = int(input('What do you want to change?\n1. Account Name\n2. Password\nEnter your choice: '))
        if ch == 1:
            newname = input('Enter the new name: ')
            c.execute("UPDATE account SET acc_name=%s WHERE password=%s", (newname, pd))
            mydb.commit()
            print('Name Updated successfully')
        elif ch == 2:
            newpassword = input('Enter the new password: ')
            c.execute("UPDATE account SET password=%s WHERE password=%s", (newpassword, pd))
            mydb.commit()
            pd = newpassword
            print('Password Updated successfully')
        else:
            print('Invalid input')
    else:
        ch = int(input('What do you want to change?\n1. Account Name\n2. Password\n3. Interest Rate\n4. Duration\nEnter your choice: '))
        if ch == 1:
            newname = input('Enter the new name: ')
            c.execute("UPDATE savings_account SET acc_name=%s WHERE password=%s", (newname, pd))
            mydb.commit()
            print('Name Updated successfully')
        elif ch == 2:
            newpassword = input('Enter the new password: ')
            c.execute("UPDATE savings_account SET password=%s WHERE password=%s", (newpassword, pd))
            mydb.commit()
            pd = newpassword
            print('Password Updated successfully')
        elif ch == 3:
            new_interest = float(input('Enter new interest rate (%): '))
            c.execute("UPDATE savings_account SET interest_rate=%s WHERE password=%s", (new_interest, pd))
            mydb.commit()
            print('Interest Rate Updated successfully')
        elif ch == 4:
            new_duration = int(input('Enter new duration (months): '))
            c.execute("UPDATE savings_account SET duration_months=%s WHERE password=%s", (new_duration, pd))
            mydb.commit()
            print('Duration Updated successfully')
        else:
            print('Invalid input')

def withdrawal():
    global bal, c, pd, no, acc_type
    print()
    amt = float(input('Enter how much you want to withdraw from the bank: '))
    
    if acc_type == 'savings':
        # Check if withdrawal is allowed (you might want to add restrictions for savings)
        print("Note: Withdrawal from savings account may affect interest calculation")
    
    if bal - amt >= 0:
        if acc_type == 'current':
            c.execute("UPDATE account SET balance=%s WHERE password=%s", (bal - amt, pd))
        else:
            c.execute("UPDATE savings_account SET balance=%s WHERE password=%s", (bal - amt, pd))
        mydb.commit()
        print(f'${amt:.2f} has been debited from your {acc_type} account')
        cb()
    else:
        print('Insufficient balance')

def deposit():
    global bal, c, pd, no, acc_type
    print()
    amt = float(input('Enter how much you want to deposit to the bank: '))
    
    if acc_type == 'current':
        c.execute("UPDATE account SET balance=%s WHERE password=%s", (bal + amt, pd))
    else:
        c.execute("UPDATE savings_account SET balance=%s WHERE password=%s", (bal + amt, pd))
    mydb.commit()
    
    if acc_type == 'current':
        c.execute("SELECT balance FROM account WHERE password=%s", (pd,))
    else:
        c.execute("SELECT balance FROM savings_account WHERE password=%s", (pd,))
    rec = c.fetchall()
    bal = rec[0][0]
    
    print(f'${amt:.2f} has been credited to your {acc_type} bank account')
    print(f'You have currently: ${bal:.2f} in your {acc_type} bank account')

def transfermoney():
    global pd, c, bal, no, acc_type
    print()
    
    # Get all accounts for transfer
    c.execute("SELECT acc_no, acc_name, 'current' as type FROM account UNION SELECT acc_no, acc_name, 'savings' as type FROM savings_account")
    rec = c.fetchall()
    
    print('\t| ACCOUNTS |')
    accounts_dict = {}
    for acc in rec:
        print(f'\t {acc[0]} - {acc[1]} ({acc[2]})')
        accounts_dict[acc[0]] = (acc[1], acc[2])
    
    print(f'Your current balance is ${bal:.2f}')
    
    try:
        target_acc = int(input('--> Enter the account number you want to transfer money to: '))
        amount = float(input('--> Enter how much money you want to transfer: '))
        
        if target_acc not in accounts_dict:
            print('Invalid account number')
            return
            
        if amount > bal:
            print('Insufficient balance')
            return
            
        # Get target account balance
        target_type = accounts_dict[target_acc][1]
        if target_type == 'current':
            c.execute("SELECT balance FROM account WHERE acc_no=%s", (target_acc,))
        else:
            c.execute("SELECT balance FROM savings_account WHERE acc_no=%s", (target_acc,))
        
        target_balance_rec = c.fetchall()
        if not target_balance_rec:
            print('Target account not found')
            return
            
        target_balance = target_balance_rec[0][0]
        
        # Update both accounts
        if acc_type == 'current':
            c.execute("UPDATE account SET balance=%s WHERE password=%s", (bal - amount, pd))
        else:
            c.execute("UPDATE savings_account SET balance=%s WHERE password=%s", (bal - amount, pd))
            
        if target_type == 'current':
            c.execute("UPDATE account SET balance=%s WHERE acc_no=%s", (target_balance + amount, target_acc))
        else:
            c.execute("UPDATE savings_account SET balance=%s WHERE acc_no=%s", (target_balance + amount, target_acc))
            
        mydb.commit()
        print('-' * 50 + ' TRANSFER SUCCESSFUL ' + '-' * 50)
        print(f'${amount:.2f} has been transferred from your {acc_type} account to account {target_acc}')
        
    except ValueError:
        print('Invalid input')

# Main program flow
print('1. Sign Up\n2. Registered Already\n3. Quit')
choice = input('Enter your choice: ')

if choice == '2':
    acc_type = input('Enter account type (current/savings): ').lower()
    pd = input('Enter your password: ')
    
    if acc_type == 'current':
        c.execute("SELECT acc_name FROM account WHERE password=%s", (pd,))
    else:
        c.execute("SELECT acc_name FROM savings_account WHERE password=%s", (pd,))
        
    rec = c.fetchall()
    if rec:
        n = rec[0][0]
    else:
        print("Invalid credentials or account type")
        exit()
elif choice == '1':
    login()
else:
    print('Invalid choice')
    exit()

no = acc_no()
if not no:
    print("Could not retrieve account number")
    exit()

cb()

while True:
    print()
    print('-' * 45)
    print('1. To Update the values')
    print('2. To Deposit money into the bank')
    print('3. To withdraw money from the bank')
    print('4. To Transfer money to another account')
    if acc_type == 'savings':
        print('5. View Interest Details')
    ch = input('Enter your choice: ')
    
    if ch == '1':
        update()
    elif ch == '2':
        deposit()
    elif ch == '3':
        withdrawal()
    elif ch == '4':
        transfermoney()
    elif ch == '5' and acc_type == 'savings':
        calculate_interest()
    else:
        print('ERROR')
        break