#%%
#The class Bank creates accounts.

class Bank:
    def __init__(self):
        self.bank_data = {}

    def add_entry(self, card_num : int, pwd : str, account, money):
        self.bank_data[card_num] = {"password":pwd, "accounts":{account:money}}

    def add_account(self, card_num, account, money):
        if card_num in self.bank_data:
            self.bank_data[card_num]["accounts"][account] = money

    def check_pwd(self, card_num, entered_pwd):
        if card_num in self.bank_data and self.bank_data[card_num]["password"] == entered_pwd:
            return self.bank_data[card_num]["accounts"]
        else:
            return None

    def update_account(self, card_num, account, money):
        if self.bank_data[card_num]["accounts"][account] in self.bank_data[card_num]["accounts"]:
            self.bank_data[card_num]["accounts"][account] = money
            return True
        else:
            return False
#%%
#The class Controller is used to operate the atm.

class Controller:
    def __init__(self, bank, cash):
        self.Bank = bank
        self.accounts = None
        self.cash_bin = cash

    def swipe(self, card_num, pwd):
        self.accounts = self.Bank.check_pwd(card_num, pwd)
        if self.accounts is None:
            return 0
        else:
            return 1

    def account_select(self, acc):
        if acc in self.accounts:
            return True
        else:
            return False

    def account_actions(self, card_num, acc, action, money=0):
        if action == "See Balance":
            return self.accounts[acc], 1
        elif action == "Withdraw":
            if self.accounts[acc] >= money and self.cash_bin >= money:
                new_balance = self.accounts[acc] - money
                self.cash_bin -= money
                self.accounts[acc] = new_balance
                self.Bank.update_account(card_num, acc, new_balance)
                return self.accounts[acc], 1
            else:
                return self.accounts[acc], 0
        elif action == "Deposit":
            new_balance = self.accounts[acc] + money
            self.cash_bin += money
            self.accounts[acc] = new_balance
            self.Bank.update_account(card_num, acc, new_balance)
            return self.accounts[acc], 1
#%%
#test bank account
test_bank = Bank()
#one
test_bank.add_entry(11111111,'1111',1123,100000)
test_bank.add_account(11111111,1234,200000)
test_bank.add_account(11111111,1345,300000)
#two
test_bank.add_entry(22222222,'2222',2123,100000)
test_bank.add_account(22222222,2234,200000)
test_bank.add_account(22222222,2345,300000)


test_bank.check_pwd(11111111,'1111')
test_bank.check_pwd(22222222,'2222')

digit = len(str(list(test_bank.bank_data.keys())[0]))

#%%
#test atm
test_atm = Controller(test_bank, 1000)
#%%

while True:
    print('Select a transaction\n')
    print('1. Start the transaction\n')
    print('2. Close the transaction\n')
    try:
        action1 = int(input('Select a number：'))
        print('')
        if action1 == 1:
            try:
                card = int(input('Please enter your card number：'))
                print('')
                if card in test_bank.bank_data.keys():
                    p_cnt = 0
                    while card:
                        pwd = input('Please enter your password.：')
                        print('')
                        valid_acc = test_atm.swipe(card, pwd)
                        if valid_acc:
                            while valid_acc:
                                print('Select a number：\n')
                                print('1. Select a account\n')
                                print('2. Return to entering card number\n')
                                try:
                                    action2 = int(input('Select a number：'))
                                    print('')
                                    if action2 == 1:
                                        acc_list=[]
                                        for i, v in enumerate(test_bank.bank_data[card]["accounts"].keys()):
                                            acc_list.append(v)
                                            print(f'{i+1}: {v}\n')
                                        try:
                                            acc = int(input('Please select your account.：'))-1
                                            if acc < len(acc_list):
                                                select_acc = 1
                                                print('')
                                                while select_acc:
                                                    print('Select a number：\n')
                                                    print('1. Account balance\n')
                                                    print('2. Deposit\n')
                                                    print('3. Withdraw\n')
                                                    print('4. Return to selecting a account\n')
                                                    print('5. Return to entering card number\n')
                                                    try:
                                                        action3 = int(input('Select a number：'))
                                                        print('')
                                                        if action3 == 1:
                                                            info, result = test_atm.account_actions(card, acc_list[acc], "See Balance", money=0)
                                                            if result:
                                                                print(f'{acc_list[acc]}, The balance is ${info}\n')
                                                            else:
                                                                print('Ask the staff\n')
                                                        elif action3 == 2:
                                                            try:
                                                                money = int(input('Enter the deposit amount:'))
                                                                print('')
                                                                info, result = test_atm.account_actions(card, acc_list[acc], "Deposit", money)
                                                                if result:
                                                                    print(f'${money} has been deposited\n')
                                                                    print(f'The balance is ${info}\n')
                                                                else:
                                                                    print('Ask the staff\n')
                                                            except:
                                                                print('')
                                                                print('Please enter numbers\n')
                                                        elif action3 == 3:
                                                            try:
                                                                money = int(input('Enter withdrawal amount:'))
                                                                print('')
                                                                info, result = test_atm.account_actions(card, acc_list[acc], "Withdraw", money)
                                                                if result:
                                                                    print(f'${money} has been withdrawn\n')
                                                                    print(f'The balance is ${info}\n')
                                                                else:
                                                                    if test_atm.accounts[acc_list[acc]] <= money:
                                                                        print('The account balance is insufficient\n')
                                                                    elif test_atm.cash_bin <= money:
                                                                        print(f'The atm balance is insufficient(${test_atm.cash_bin})\n')
                                                            except:
                                                                print('')
                                                                print('Please enter numbers\n')
                                                        elif action3 == 4:
                                                            select_acc = 0
                                                            break
                                                        elif action3 == 5:
                                                            select_acc = 0
                                                            valid_acc = 0
                                                            card = 0
                                                            break
                                                        else:
                                                            print('Select a number on the screen\n')
                                                    except:
                                                        print('')
                                                        print('Select a number on the screen\n')
                                            else:
                                                print('')
                                                print('Select a account on the screen\n')
                                        except:
                                            print('')
                                            print('Select a account on the screen\n')
                                    elif action2 == 2:
                                        card = 0
                                        break
                                    else:
                                        print('Select a number on the screen\n')
                                except:
                                    print('')
                                    print('Select a number on the screen\n')
                        else:
                            p_cnt += 1
                            print(f'Password mismatch: {p_cnt}\n')
                        if p_cnt == 3:
                            card = 0
                            break
                else:
                    print('The card numbers do not match\n')
            except:
                print('')
                print(f'The card number is {digit} digits\n')
        elif action1 == 2:
            break
        else:
            print('Select a number on the screen\n')
    except:
        print('')
        print('Select a number on the screen\n')
