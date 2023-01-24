from tabulate import tabulate


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
        output = f"{yellow}{underline}///////////////////////////////////{end}\n"
        output += f"{pink}Country:{end} {self.country}\n"
        output += f"{pink}Code:{end} {self.code}\n"             # Prevents the user having to enter SKU each time.
        output += f"{pink}Product name:{end} {self.product}\n"
        output += f"{pink}Cost:{end} £{self.cost}\n"
        output += f"{pink}Quantity:{end} {self.quantity} pairs\n"
        output += f"{yellow}{underline}///////////////////////////////////{end}\n"
        return output


# #==========Functions outside the class==============
def read_shoes_data():
    """ Takes data from "inventory.txt" and converts each line into a new object, which then gets appended to
    the shoe_list.
    :return: (list) Contains all data from inventory.txt, ready to print and formatted for a table.
    """
    # shoe_list = []
    # read_object = None
    table = []
    # shoes = None
    try:
        read_file = open("inventory.txt", "r", encoding="UTF-8")
        header = read_file.readline()         # Removes header for objects.
        inventory = read_file.readlines()
        read_file.close()

    except FileNotFoundError:
        print(f"\n{red}The inventory.txt file could not be found."
              f"\nPlease check that it hasn't been renamed or relocated before trying again.{end}")

    if len(inventory) > 0:
        header_split = header.split(",")
        table = [header_split]

        for read in inventory:
            shoes = read.split(",")
            table.append(shoes)                 # Lists of shoes.
            read_object = Shoe(shoes[0], shoes[1], shoes[2], shoes[3], shoes[4])
            shoe_list.append(read_object)       # Shoe objects list.
        print(f"{green}The system has been updated with a full inventory of all products.{end}")
    else:
        print(f"{yellow}The inventory.txt file exists but contains no data.{end}\n"
              f"Go to Add Product to update the inventory")
    # print(table)
    return table


def add_product():
    """ This method creates a Shoe object by taking in user inputs. """
    read_shoes_data()
    code = None
    cost = None
    in_stock = None

    country = input("Which country produces the shoe: ").title()
    product_name = input("What is the product name of the shoe: ").title()

    while True:
        try:
            code = int(input("Please enter the product code: SKU"))    # The code is input straight after SKU.
            cost = int(input("What is the sale price for each pair: £"))
            in_stock = int(input("How many pairs are in stock: "))     # Quantity.
            break
        except ValueError:          # Integer inputs only.
            print(f"\n{red}The inputs for code, cost and quantity specifically require numbers to be entered."
                  f"Please try again.{end}")
            continue

    product_code = f"SKU{code}"

    new_object = Shoe(country, product_code, product_name, cost, in_stock)
    # A string data-type version of the "new_object" which can now be appended to the "inventory.txt" file.
    write_list = ["\n" + country + ",", "SKU" + str(code) + ",", product_name + ",", str(cost) + ",", str(in_stock)]
    print(f"{green}{product_name}s have been added to the inventory.{end}")

    shoe_list.append(new_object)

    f = open("inventory.txt", "a", encoding="UTF-8")
    for each in write_list:
        f.write(each)
    f.close()


def view_all():
    """ Outputs each pair of shoes and their data from the inventory neatly within a table. """
    table = read_shoes_data()
    header = table[0]
    table.pop(0)
    for each in table:
        each[3] = "£" + each[3]
    table.insert(0, header)
    print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))
    print("\n")     #test


def stock_quantities(min_max=min):
    """ Determines which product has the lowest quantity stored and gives the option to restock whilst updating
    the quantity value.
    """
    read_shoes_data()
    quantities_list = []
    for shoe in shoe_list:          # Table? converts to string
        quantities_list.append(int(shoe.get_quantity()))      # get_quant?
    stock_quantity = min_max(quantities_list)
    return stock_quantity


def re_stock():
    """ Determines the product with the lowest stock and asks how many pairs should be purchased.
    The inventory is then updated with the new quantity.
    """
    table = read_shoes_data()
    lowest_quantity = stock_quantities(min)
    additional_stock = 0

    for index, shoe in enumerate(shoe_list, start=1):
        if lowest_quantity == int(shoe.get_quantity()):
            print(shoe)

            while True:
                try:
                    additional_stock = int(input(f"How many pairs of {shoe.get_product()}s would you like to buy: "))
                    break
                except ValueError:
                    print(f"{red}Please enter the amount of pairs you would like to add as a whole number.{end}\n")
                    continue
                # break

            # Combines the current product quantity and the additional_stock input.
            new_quantity = shoe.increase_quantity(shoe.get_quantity(), additional_stock)
            restocked = index

            restock_cost = additional_stock * int(shoe.get_cost())
            if 0 < additional_stock:
                print(f"{green}Your order of {additional_stock} pairs of {shoe.get_product()}s has been dispatched and "
                      f"will be shipped to your depot.\n"
                      f"An invoice of £{restock_cost} will be sent to you.{end}\n\n"
                      f"This is an updated view of the products stock count.")
                print(shoe)
            else:
                print(f"{red}No pairs were ordered, we look forward to your next order.{end}")
            break



    table[restocked][4] = new_quantity
    print(table)
    inventory_file = open("inventory.txt", "w+", encoding="UTF-8")

    p = []
    # for each in table:
    #     join2 = ",".join(str(each))
    #     p.append(join2)
    # join2 = " ".join(table)
    # print(join2)
    # print(p)

    for each in table:
        z4 = ",".join(str(each))
        for a in each:
            print(z4)
            print(a)
            z3 = ",".join(str(a))
            inventory_file.write(str(a))


        # join2 = ",".join(str(each))
        # p.append(join2)
    # join2 = " ".join(table)
    # print(join2)
    # print(p)
    # print(z3)
        # tab = str(each)


    # inventory_file.write(str(tab))
    print(z3)


def search_shoe():
    """ Input an SKU code for a shoe and this method will return the object if it is inside "shoe_list"."""
    # read_shoes_data()
    shoe_id = input("Which SKU code would you like to search for: ").upper()
    for shoe in shoe_list:
        if shoe.get_code() == shoe_id:
            return shoe

    return f"{red}Please enter a valid product SKU code to search the system.{end}"


def highest_qty():
    highest_quantity = stock_quantities(max)
    print("\nHighest product stock count")
    for shoe in shoe_list:
        # Checks which object in the "shoe_list" has the same stock count as the object with the "max_quantity".
        if highest_quantity == int(shoe.get_quantity()):
            print(shoe)
            print(f"{red}The {shoe.product}s are overstocked and will now be placed on sale.{end}")
            break


def product_stock_cost():
    """ Calculates the total cost of each product in stock and outputs the data in a table format. """
    # read_shoes_data()
    table = [["Product", "Individual Cost", "Quantity", "Total Value"]]

    for shoe in shoe_list:
        total_value_list = []
        cost = "£" + (shoe.get_cost())
        total = int(shoe.get_cost()) * int(shoe.get_quantity())
        cost_total = "£" + str(total)
        total_value_list.append(shoe.get_product())
        total_value_list.append(cost)
        total_value_list.append(shoe.get_quantity())
        total_value_list.append(cost_total)
        table.append(total_value_list)

    print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))


# Variables for modifying text styles.
pink = '\033[95m'
blue = '\033[94m'
cyan = '\033[96m'
green = '\033[92m'
yellow = '\033[93m'
red = '\033[91m'
end = '\033[0m'
bold = '\033[1m'
underline = '\033[4m'

shoe_list = []
# read_inventory = read_shoes_data()

# #==========Main Menu=============
while True:
    menu = input(f"\n\t {red}{underline}Inventory Menu{end}\n"
                 # f"\t {blue}1:  {cyan}Read File\n"
                 f"\t {blue}2:  {cyan}Add Product\n"
                 f"\t {blue}3:  {cyan}View All Products\n"
                 f"\t {blue}4:  {cyan}Restock Inventory\n"
                 f"\t {blue}5:  {cyan}Highest In-Stock\n"
                 f"\t {blue}6:  {cyan}Search Product\n"
                 f"\t {blue}7:  {cyan}Product Stock Cost{end}\n"
                 ": ")
    print("\n")
    if menu == "1":
        print("1: Read File")
        read_shoes_data()

    elif menu == "2":
        print("2: Add Product")
        add_product()

    elif menu == "3":
        print("3: View All Products")
        view_all()

    elif menu == "4":
        print("4: Restock Inventory")
        re_stock()

    elif menu == "5":
        print("5: Highest In-Stock")
        highest_qty()

    elif menu == "6":
        print("6: Search Product")
        print(search_shoe())

    elif menu == "7":
        print("7: Product Stock Cost")
        product_stock_cost()
        # shoe_list = []

    else:
        print(f"{red}Please enter the number relevant to the menu option.{end}")


# TODO: Error handling.
