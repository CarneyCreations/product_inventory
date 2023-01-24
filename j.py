import csv
shoe_list = []


class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_code(self):
        return self.code

    def get_product(self):
        return self.product

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def increase_quantity(self, current_quantity, additional_stock):
        self.quantity = int(additional_stock) + int(current_quantity)
        return self.quantity

    def __str__(self):
        output = f"///////////////////////////////////\n"
        output += f"Country: {self.country}\n"
        output += f"Code: {self.code}\n"             # Prevents the user having to enter SKU each time.
        output += f"Product name: {self.product}\n"
        output += f"Cost: £{self.cost}\n"
        output += f"Quantity: {self.quantity} pairs\n"
        output += f"///////////////////////////////////\n"
        return output




def read_shoes_data():
    """ Takes data from "inventory.txt" and converts each line into a new object, which then gets appended to
    the shoe_list.
    :return: (list) Contains all data from inventory.txt, ready to print and formatted for a table.
    """
    global shoe_list
    header_split = []
    table = []
    try:
        read_file = open("inventory.txt", "r", encoding="UTF-8")
        header = read_file.readline()         # Removes header for objects.
        inventory = read_file.readlines()
        read_file.close()
        header_split = header.split(",")
        for read in inventory:
            stripped = read.strip("\n")
            shoes = stripped.split(",")
            table.append(shoes)                 # Lists of shoes.
            read_object = Shoe(shoes[0], shoes[1], shoes[2], shoes[3], shoes[4])
            shoe_list.append(read_object)       # Shoe objects list.

    except FileNotFoundError:
        print(f"\nThe inventory.txt file could not be found."
              f"\nPlease check that it hasn't been renamed or relocated before trying again.")
    # print(table)
    return header_split, table


def stock_quantities(min_max=min):
    """ Determines which product has the lowest quantity stored and gives the option to restock whilst updating
    the quantity value.
    """
    header_split, table = read_shoes_data()
    quantities_list = []
    for shoe in shoe_list:          # Table? converts to string
        quantities_list.append(int(shoe.quantity))      # get_quant?
    stock_quantity = min_max(quantities_list)
    return stock_quantity


def re_stock():
    """ Determines the product with the lowest stock and asks how many pairs should be purchased.
    The inventory is then updated with the new quantity.
    """

    # restocked = 0
    new_quantity = 0
    header, table = read_shoes_data()
    lowest_quantity = stock_quantities(min)
    additional_stock = 0

    for index, shoe in enumerate(shoe_list, start=1):
        if lowest_quantity == int(shoe.get_quantity()):
        #     print(shoe)

            while True:
                try:
                    additional_stock = int(input(f"How many pairs of {shoe.get_product()}s would you like to buy: "))
                except ValueError:
                    print(f"Please enter the amount of pairs you would like to add as a whole number.\n")
                    table[index][4] = new_quantity
                    print(table[index][4])
                    continue

                break

            # Combines the current product quantity and the additional_stock input.
            new_quantity = shoe.increase_quantity(int(shoe.get_quantity()), additional_stock)
            print(f"New_quantity {new_quantity}")
            restocked = index
            print(f"Restocked {restocked}")
            restock_cost = additional_stock * int(shoe.get_cost())
            if 0 < additional_stock:
                print(f"Your order of {additional_stock} pairs of {shoe.get_product()}s has been dispatched and "
                      f"will be shipped to your depot.\n"
                      f"An invoice of £{restock_cost} will be sent to you.\n\n"
                      f"This is an updated view of the products stock count.")
                print(shoe)
            else:
                print(f"No pairs were ordered, we look forward to your next order.")
            break

        # print(table[index][4])
        table[index][4] = new_quantity
        table[1][4] = new_quantity
        print(f"table {table[index][4]}")

    # inventory_file = open("inventory.txt", "a+", encoding="UTF-8")
    #
    #
    # for each in table:
    #     # z4 = ",".join(str(each))
    #     for a in each:
    #         # print(f"z4{z4}")
    #         print(f"a{a}")
    #         # z3 = ",".join(str(a))
    #         inventory_file.write(str(a))



header, table = read_shoes_data()
re_stock()
csv_data = []

# binance_csv = open("inventory.txt",
#                    "r", encoding="ISO-8859-1")
binance_csv = open("test.csv",
                   "r", encoding="ISO-8859-1")
# Converts from a TextIOWrapper to a csv.reader object.
csvreader = csv.reader(binance_csv)

# Adds the first row (header) to "csv_header" and iterates to the second row.
csv_header = next(csvreader)

# Converts from a csv.reader object in to a list.
for row in csvreader:
    csv_data.append(row)
# binance_csv.close()
print(csv_data)


csvfile = open("test.csv", 'w+')
    # creating a csv writer object
csvwriter = csv.writer(csvfile)

# writing the fields
csvwriter.writerow(header)

# writing the data rows
# csvwriter.writerows(csv_data)
csvwriter.writerows(table)
print(csv_data)
print(table)

