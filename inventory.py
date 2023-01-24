from tabulate import tabulate
from datetime import datetime


class Shoe:
    """ Shoe class defined."""
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
        output = f"{yellow}{underline}/////////////////////////////{end}\n"
        output += f"{pink} Country:{end} {self.country}\n"
        output += f"{pink} Code:{end} {self.code}\n"             # Prevents the user having to enter SKU each time.
        output += f"{pink} Product name:{end} {self.product}\n"
        output += f"{pink} Cost:{end} £{self.cost}\n"
        output += f"{pink} Quantity:{end} {self.quantity} pairs\n"
        output += f"{yellow}{underline}/////////////////////////////{end}\n"
        return output


def read_shoes_data():
    """ Takes data from "inventory.txt" and converts each line into a new object, which then gets appended to
    the shoe_list.
    :return: (list) Contains all data from inventory.txt, ready to print and formatted for a table.
    """
    inventory_data = ""             # String variable needed for the len() checking the file contains data.
    shoe_strings_list = []
    header = None

    # Read from the inventory.txt file
    try:
        read_inventory = open("inventory.txt", "r", encoding="UTF-8")
        header = read_inventory.readline()         # Removes header for objects.
        inventory_data = read_inventory.readlines()
        read_inventory.close()

    except FileNotFoundError:
        print(f"\n{red} The inventory.txt file could not be found."
              f"\n Please check that it hasn't been renamed or relocated before trying again.{end}")

    # If file is found and contains data.
    if len(inventory_data) > 0:
        split_header = header.split(",")
        shoe_strings_list = [split_header]

        # From the text file, this creates a list of strings and a list of Shoe objects.
        for read in inventory_data:
            shoes = read.split(",")
            shoe_strings_list.append(shoes)                                          # Shoe string list.
            read_object = Shoe(shoes[0], shoes[1], shoes[2], shoes[3], shoes[4])
            shoe_list.append(read_object)                                           # Shoe objects list.
        print(f"————————————————————————————————————————————————————————————————————\n"
              f"{green} The system has been updated with a full inventory of all products.{end}\n"
              f"————————————————————————————————————————————————————————————————————")

    # Triggers if the file is located but is empty.
    elif len(inventory_data) < 1:
        print(f"{yellow} The inventory.txt file exists but contains no data.{end}\n"
              f" Go to Add Product to update the inventory")
    return shoe_strings_list


def add_product():
    """ This function creates a Shoe object from user inputs and updates "inventory.txt" with the new product. """
    code = None
    cost = None
    in_stock = None

    country = input(" Which country produces the shoe: ").title()
    product_name = input(" What is the product name of the shoe: ").title()

    while True:
        try:
            code = int(input(" Please enter the product code: SKU"))            # The code is input straight after SKU.
            cost = int(input(" What is the sale price for each pair: £"))
            in_stock = int(input(" How many pairs are in stock: "))             # Quantity.
            break
        except ValueError:          # Integer inputs only.
            print(f"\n{red} The inputs for code, cost and quantity specifically require numbers to be entered."
                  f"\n Please try again.{end}")
            continue

    product_code = f"SKU{code}"

    # Shoe object created from inputs and added to the Shoe objects list.
    new_object = Shoe(country, product_code, product_name, cost, in_stock)
    shoe_list.append(new_object)

    # A string equivalent of the Shoe object which can be appended to the "inventory.txt" file.
    write_list = ["\n" + country + ",", "SKU" + str(code) + ",", product_name + ",", str(cost) + ",", str(in_stock)]
    print(f" {green}{product_name}s have been added to the inventory.{end}")

    # Append new inventory item to the text file.
    f = open("inventory.txt", "a", encoding="UTF-8")
    for each in write_list:
        f.write(each)
    f.close()


def view_all():
    """ Takes each product and the associated data from "inventory.txt" and outputs it within a table. """
    header = string_shoe_list[0]
    shoe_string_gbp = string_shoe_list
    shoe_string_gbp.pop(0)

    for each in shoe_string_gbp:
        each[3] = "£" + each[3]

    shoe_string_gbp.insert(0, header)
    print(tabulate(string_shoe_list, headers="firstrow", tablefmt="fancy_grid") + "\n")
    read_shoes_data()


def stock_quantities(min_max=min):
    """ Depending on the parameter, this determines which product has the lowest/highest quantity stored and gives
    the option to restock whilst updating the quantity value.
    :param: (function) Min() or max() are the intended functions to be entered. The min() function is called by
            default if there are no entries.
    :return: (int) The highest or lowest stock value of a product, depending on the parameter.
    """
    quantities_list = []
    for shoe in shoe_list:
        quantities_list.append(int(shoe.get_quantity()))
    stock_quantity = min_max(quantities_list)
    return stock_quantity


def re_stock():
    """ Takes the product with the lowest quantity from stock_quantities and asks how many more pairs should be
    ordered.
    Determines the product with the lowest stock and asks how many pairs should be purchased.
    The inventory is then updated with the new quantity.
    """
    lowest_quantity = stock_quantities(min)
    additional_stock = 0

    # Compares the Shoe objects, looking for the product with the lowest quantity.
    for index, shoe in enumerate(shoe_list, start=1):
        if lowest_quantity == int(shoe.get_quantity()):
            print(shoe)

            while True:
                try:
                    additional_stock = int(input(f"How many pairs of {shoe.get_product()}s would you like to buy: "))
                    break
                except ValueError:
                    print(f"{red} Please enter the amount of pairs you would like to add as a whole number.{end}\n")
                    continue

            # Totals the current stock levels of the product and also the amount being bought.
            new_quantity = shoe.increase_quantity(shoe.get_quantity(), additional_stock)

            # Creates a list containing the restocked product.
            string_shoe_list[index] = [shoe.country, str(shoe.get_code()), str(shoe.get_product()),
                                       str(shoe.get_cost()), str(new_quantity) + "\n"]

            # Used in the display message as an invoice.
            restock_cost = additional_stock * int(shoe.get_cost())

            if 0 < additional_stock:
                print(f"\n\n—————————————————————————————————————————————————————————————————————\n"
                      f"{green} Your order of {additional_stock} pairs of {shoe.get_product()}s has been dispatched "
                      f"and will \n be shipped to your depot. Please find you invoice attached.{end}\n"
                      f"—————————————————————————————————————————————————————————————————————\n\n\n\n")

                # Invoice written into lists, ready for tabulate.
                invoice_header = [f"New order:            {pink}CarneyCreations{end}"]
                invoice_body = [[f"{pink}Shoe Style:{end}           {shoe.get_product()}\n"],
                                [f"{pink}Product Code:{end}         {shoe.get_code()}\n"],
                                [f"{pink}Quantity Ordered:{end}     {additional_stock}\n"],
                                [f"{pink}Individual Price:{end}     £{shoe.get_cost()}\n"],
                                [f"========================================\n"],
                                [f"Total Cost:          {red}£{restock_cost}{end}\n\n"],
                                ]
                date = datetime.now()
                print(date.strftime("%d %B %Y"), "\nInvoice")
                print(tabulate(invoice_body, invoice_header, tablefmt="rst"), "\n\n\n\n\n")
                print(shoe)
            else:
                print(f"{red} No pairs were ordered, we look forward to your next order.{end}")
            break

    # Rewrites all product related information to the "inventory.txt" file.
    inventory_file = open("inventory.txt", "w+", encoding="UTF-8")

    for product in string_shoe_list:
        for column, product_info in enumerate(product):
            if column < 4:                                      # In a column, separate the values.
                updated_products = product_info + ","
            else:                                               # If in the last column add a new line.
                updated_products = product_info
            inventory_file.write(str(updated_products))


def highest_qty():
    """ Takes the product with the highest quantity from the stock_quantities function, matches it with a
    product before displaying it.
    """
    highest_quantity = stock_quantities(max)
    print(" Highest product stock count")
    for shoe in shoe_list:

        # Checks which object in the "shoe_list" has the same stock count as the object with the "max_quantity".
        if highest_quantity == int(shoe.get_quantity()):
            print(shoe)
            print(f"{red} The {shoe.product}s are overstocked and will now be placed on sale.{end}")
            break


def search_shoe():
    """ Input an SKU code for a shoe and this function will return the object if it is on record.
    :return: Either the Shoe object which the user is looking for is returned or an error output.
    """
    shoe_id = input(" Which SKU code would you like to search for: ").upper()
    for shoe in shoe_list:
        if shoe.get_code() == shoe_id:
            print("\n")
            return shoe
    return f"{red} Please enter a valid product SKU code to search the system.{end}"


def product_stock_cost():
    """ Calculates the total inventory cost of each product and outputs the data in a table format. """
    stock_cost_table = [["Product", "Individual Cost", "Quantity", "Total Value"]]

    for shoe in shoe_list:
        total_value_list = []

        total = (int(str(shoe.cost))) * (int(shoe.quantity))
        cost = "£" + str((shoe.get_cost()))
        cost_total = "£" + str(total)
        total_value_list.append(shoe.get_product())
        total_value_list.append(cost)
        total_value_list.append(shoe.get_quantity())
        total_value_list.append(cost_total)
        stock_cost_table.append(total_value_list)

    print(tabulate(stock_cost_table, headers="firstrow", tablefmt="fancy_grid"))


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


# Main menu section.
while True:
    menu = input(f"\n\n\n\t {red}{underline}    Inventory Menu  {end}\n"
                 f"\t {blue}1:  {cyan}Add Product\n"
                 f"\t {blue}2:  {cyan}View All Products\n"
                 f"\t {blue}3:  {cyan}Restock Inventory\n"
                 f"\t {blue}4:  {cyan}Highest In-Stock\n"
                 f"\t {blue}5:  {cyan}Search Product\n"
                 f"\t {blue}6:  {cyan}Product Stock Cost{end}\n"
                 " >> ")
    print("\n")
    string_shoe_list = read_shoes_data()
    print("\n\n")

    if menu == "1":
        print(f"\t {red}{bold}{underline}  Add Product  {end}\n")
        add_product()

    elif menu == "2":
        print(f"\t {red}{bold}{underline} View All Products  {end}\n")
        view_all()

    elif menu == "3":
        print(f"\t {red}{bold}{underline}  Restock Inventory  {end}\n")
        re_stock()
        read_shoes_data()                            # Updates text file with additional stock.

    elif menu == "4":
        print(f"\t {red}{bold}{underline}  Highest In-Stock  {end}\n")
        highest_qty()

    elif menu == "5":
        print(f"\t {red}{bold}{underline}  Search Product  {end}\n")
        print(search_shoe())

    elif menu == "6":
        print(f"\t {red}{bold}{underline}  Product Stock Cost  {end}\n")
        shoe_list = []                               # Avoids multiple object lists within this variable.
        read_shoes_data()                            # Otherwise there is no data and an empty table is printed.
        product_stock_cost()

    else:
        print(f"{red} Please enter the number relevant to the menu option.{end}")
