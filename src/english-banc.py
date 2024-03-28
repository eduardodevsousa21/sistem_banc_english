import textwrap

def menu():
    menu_text = """\n
    ================ MENU ================
    [d]\tDeposit
    [w]\tWithdraw
    [s]\tStatement
    [nc]\tNew account
    [lc]\tList accounts
    [nu]\tNew user
    [q]\tQuit
    => """
    return input(textwrap.dedent(menu_text))


def deposit(balance, amount, statement):
    if amount > 0:
        balance += amount
        statement += f"Deposit:\t\t$ {amount:.2f}\n"
        print("\n=== Deposit successful! ===")
    else:
        print("\n@@@ Operation failed! The entered amount is invalid. @@@")

    return balance, statement


def withdraw(*, balance, amount, statement, limit, num_withdrawals, withdrawal_limit):
    exceeds_balance = amount > balance
    exceeds_limit = amount > limit
    exceeds_withdrawals = num_withdrawals >= withdrawal_limit

    if exceeds_balance:
        print("\n@@@ Operation failed! You do not have sufficient balance. @@@")

    elif exceeds_limit:
        print("\n@@@ Operation failed! The withdrawal amount exceeds the limit. @@@")

    elif exceeds_withdrawals:
        print("\n@@@ Operation failed! Maximum number of withdrawals exceeded. @@@")

    elif amount > 0:
        balance -= amount
        statement += f"Withdrawal:\t$ {amount:.2f}\n"
        num_withdrawals += 1
        print("\n=== Withdrawal successful! ===")

    else:
        print("\n@@@ Operation failed! The entered amount is invalid. @@@")

    return balance, statement


def display_statement(balance, /, *, statement):
    print("\n================ STATEMENT ================")
    print("No transactions have been made." if not statement else statement)
    print(f"\nBalance:\t\t$ {balance:.2f}")
    print("===========================================")


def create_user(users):
    cpf = input("Enter the CPF (numbers only): ")
    user = filter_user(cpf, users)

    if user:
        print("\n@@@ User with this CPF already exists! @@@")
        return

    name = input("Enter the full name: ")
    birth_date = input("Enter the date of birth (dd-mm-yyyy): ")
    address = input("Enter the address (street, number - district - city/state): ")

    users.append({"name": name, "birth_date": birth_date, "cpf": cpf, "address": address})

    print("=== User created successfully! ===")


def filter_user(cpf, users):
    filtered_users = [user for user in users if user["cpf"] == cpf]
    return filtered_users[0] if filtered_users else None


def create_account(branch, account_number, users):
    cpf = input("Enter the user's CPF: ")
    user = filter_user(cpf, users)

    if user:
        print("\n=== Account created successfully! ===")
        return {"branch": branch, "account_number": account_number, "user": user}

    print("\n@@@ User not found, account creation process terminated! @@@")


def list_accounts(accounts):
    for account in accounts:
        line = f"""\
            Branch:\t{account['branch']}
            A/C:\t\t{account['account_number']}
            Holder:\t{account['user']['name']}
        """
        print("=" * 100)
        print(textwrap.dedent(line))


def main():
    WITHDRAWAL_LIMIT = 3
    BRANCH = "0001"

    balance = 0
    limit = 500
    statement = ""
    num_withdrawals = 0
    users = []
    accounts = []

    while True:
        option = menu()

        if option == "d":
            amount = float(input("Enter the deposit amount: "))

            balance, statement = deposit(balance, amount, statement)

        elif option == "w":
            amount = float(input("Enter the withdrawal amount: "))

            balance, statement = withdraw(
                balance=balance,
                amount=amount,
                statement=statement,
                limit=limit,
                num_withdrawals=num_withdrawals,
                withdrawal_limit=WITHDRAWAL_LIMIT,
            )

        elif option == "s":
            display_statement(balance, statement=statement)

        elif option == "nu":
            create_user(users)

        elif option == "nc":
            account_number = len(accounts) + 1
            account = create_account(BRANCH, account_number, users)

            if account:
                accounts.append(account)

        elif option == "lc":
            list_accounts(accounts)

        elif option == "q":
            break

        else:
            print("Invalid operation, please select the desired operation again.")


main()
