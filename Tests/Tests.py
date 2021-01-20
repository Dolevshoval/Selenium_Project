import unittest
from selenium.webdriver.common.keys import Keys
from Web_Pages.Main_Page import Main_Page
from Web_Pages.Category_Page import Category_Page
from Web_Pages.Product_Page import Product_Page
from Web_Pages.Pop_up_checkout import Pop_up_checkout
from Web_Pages.Cart_Page import Cart_Page
from Web_Pages.OrderPaymentLogin_Page import OrderPaymentLogin
from Web_Pages.CreateAccount_Page import CreateAccount
from Web_Pages.PaymentMethod_Page import PaymentMethod_Page
from Web_Pages.PageBase import PageBase
import time


class AOS_TESTS(unittest.TestCase):
    # a function that adds products to the cart, we use this a lot
    def add_product_to_cart(self, quantity):
        self.product_page.change_quantity(quantity)  # change product quantity
        self.product_page.add_to_cart()

    def setUp(self):
        self.main_page = Main_Page()
        self.main_page.get_main_page()
        self.main_page.driver.delete_all_cookies()
        time.sleep(3)
        self.main_page.driver.maximize_window()

    # test 1
    def test_1(self):
        self.main_page.click_on_category('tablets')
        self.category_page = Category_Page()         # click on the category page
        self.category_page.scan_and_click()
        self.product_page = Product_Page()
        self.add_product_to_cart(3)
        self.product_page.go_back()
        self.category_page.scan_and_click()
        self.add_product_to_cart(2)

        # assertion - checking the total number of products in the cart
        self.pop_out = Pop_up_checkout()
        total = self.pop_out.get_total_quantity().text
        self.assertEqual(total, '(5 Items)')

    def test_2(self):
        self.main_page.click_on_category('tablets')
        self.category_page = Category_Page()  # click on the category page
        self.category_page.scan_products()  # get the list of the products that are in stock from the page
        self.category_page.click_on_product()  # click on some product
        self.product_page1 = Product_Page()  # create instance
        self.product_page1.change_quantity(3)  # change product quantity
        self.product_page1.choose_color()  # choose color
        self.product_page1.add_to_cart()  # adding to cart
        p1 = [self.product_page1.name, self.product_page1.color, self.product_page1.quantity]  # save product parameters
        self.p1_pop_up = Pop_up_checkout()
        p1_pop_up = [self.p1_pop_up.name, self.p1_pop_up.color, self.p1_pop_up.quantity]  # save pop_up parameters of this product
        self.main_page.get_main_page()  # back to main page
        self.main_page.click_on_category('mice')
        self.category_page.scan_products()  # get the list of the products that are in stock from the page
        self.category_page.click_on_product()
        self.product_page2 = Product_Page()
        self.product_page2.change_quantity(5)  # change product quantity
        self.product_page2.choose_color()
        self.product_page2.add_to_cart()
        p2 = [self.product_page2.name, self.product_page2.color, self.product_page2.quantity]
        self.p2_pop_up = Pop_up_checkout()
        p2_pop_up = [self.p2_pop_up.name, self.p2_pop_up.color, self.p2_pop_up.quantity]
        self.main_page.get_main_page()
        self.main_page.click_on_category('headphones')
        self.category_page.scan_products()
        self.category_page.click_on_product()
        self.product_page3 = Product_Page()
        self.product_page3.change_quantity(8)
        self.product_page3.choose_color()
        self.product_page3.add_to_cart()
        self.pop_up_checkout = Pop_up_checkout()
        p3 = [self.product_page3.name, self.product_page3.color, self.product_page3.quantity]
        self.p3_pop_up = Pop_up_checkout()
        p3_pop_up = [self.p3_pop_up.name, self.p3_pop_up.color, self.p3_pop_up.quantity]
        self.assertEqual(p1, p1_pop_up)
        self.assertEqual(p2, p2_pop_up)
        self.assertEqual(p3, p3_pop_up)

    def test_3(self):
        self.main_page.click_on_category('tablets')
        self.category_page = Category_Page()  # click on the category page
        self.category_page.scan_and_click()
        self.product_page = Product_Page()
        self.add_product_to_cart(3)
        self.product_page.go_back()
        self.category_page.scan_products()  # get the list of the products that are in stock from the page
        self.category_page.click_on_product()
        self.add_product_to_cart(2)
        self.product_page.go_back()
        # removing a product from the popup cart
        self.pop_out = Pop_up_checkout()
        self.pop_out.remove_product()

        # assertion - checking the total number of products in the cart
        self.pop_out = Pop_up_checkout()
        total = self.pop_out.get_total_quantity().text
        self.assertNotEqual(total, '(5 Items)')  # checks if only first products quantity left by comparing to the
        # previous total

    def test_4(self):
        # making an order:
        self.main_page.click_on_category('speakers')
        self.category_page = Category_Page()
        self.category_page.scan_and_click()
        self.product_page = Product_Page()
        self.add_product_to_cart(5)
        self.cart_page = Cart_Page()
        self.cart_page.go_to_cart()  # go to cart page
        location = self.cart_page.get_page_path().text  # checks page path
        print(location, " is SHOPPING CART PAGE")
        self.assertIn("SHOPPING CART", location)

    def test_5(self):
        self.main_page.click_on_category('tablets')
        self.category_page = Category_Page()  # click on the category page
        self.category_page.scan_and_click()
        self.product_page = Product_Page()
        self.add_product_to_cart(3)
        price1 = self.product_page.get_price()
        self.product_page.go_back()
        self.category_page.scan_and_click()
        self.add_product_to_cart(2)
        price2 = self.product_page.get_price()
        self.product_page.go_back()  # go back to the category page
        self.product_page.go_back()  # go back to the main page aka category menu
        self.main_page.click_on_category('speakers')  # trying different category
        self.category_page.scan_and_click()
        self.add_product_to_cart(4)
        price3 = self.product_page.get_price()
        # go to cart page
        self.cart_page = Cart_Page()
        self.pop_out = Pop_up_checkout()
        self.cart_page.go_to_cart()
        cart_price = self.cart_page.get_price()  # get total cart price
        # compare each ones price summed to the cart page total price at the end
        total_price = 3*price1 + 2*price2 + 4*price3 # sums prices we got from each page multiplied by the quantity
        self.assertEqual(cart_price, total_price)

    def test_6(self):
        self.main_page.click_on_category('headphones')
        self.category_page = Category_Page()  # click on the category page
        self.category_page.scan_and_click()
        self.product_page = Product_Page()
        self.add_product_to_cart(3)
        self.product_page.go_back()
        self.category_page.scan_and_click()
        self.add_product_to_cart(2)
        # go to cart page
        self.cart_page = Cart_Page()
        self.cart_page.go_to_cart()
        time.sleep(6)  # wait for popup cart to disappear
        # get the list of current quantities on page
        list1 = self.cart_page.get_quantity_list()  # list of the first  2 product quantities
        print(list1)
        self.cart_page.edit_quantity(1)  # goes to edit the products in the first row
        self.add_product_to_cart(5)  # changes to 5 of that product and goes to cart
        # change the second product quantity
        self.cart_page.edit_quantity(2)
        self.add_product_to_cart(4)
        # go to cart page
        self.cart_page.go_to_cart()
        list2 = self.cart_page.get_quantity_list()  # list of the new product quantities
        print(list2)
        self.assertNotEqual(list1[0], list2[0])  # comparing both products
        self.assertNotEqual(list1[1], list2[1])  # comparing both products

    def test_7(self):
        main_page_url = self.main_page.get_current_url()  # get main page URL
        self.main_page.click_on_category('tablets')
        self.category_page = Category_Page()  # click on the category page
        tablet_url = self.main_page.get_current_url()  # get current URL
        self.category_page.scan_products()  # get the list of the products that are in stock from the page
        self.category_page.click_on_product()  # click on some product
        self.product_page = Product_Page()  # create instance
        self.product_page.add_to_cart()  # adding to cart
        self.main_page.go_back()  # go page back
        current_url = self.main_page.get_current_url() # get current URL after back page
        self.assertEqual(tablet_url, current_url)
        self.main_page.go_back()
        check_main_page_url = self.main_page.get_current_url()
        self.assertEqual(main_page_url, check_main_page_url)

    def test_8(self):
        self.main_page.click_on_category('tablets')
        self.category_page = Category_Page()  # click on the category page
        self.category_page.scan_products()  # get the list of the products that are in stock from the page
        self.category_page.click_on_product()  # click on some product
        self.product_page1 = Product_Page()  # create instance
        self.product_page1.add_to_cart()  # adding to cart
        product_name = self.product_page1.name
        self.pop_up_checkout = Pop_up_checkout()
        self.pop_up_checkout.click_to_checkout()
        self.order_payment_login = OrderPaymentLogin()
        self.order_payment_login.click_to_register()
        self.create_account = CreateAccount()
        self.create_account.enter_valid_details()
        self.order_payment_login.click_next()
        self.payment_method = PaymentMethod_Page()
        self.payment_method.pay_with_safepay()
        self.assertEqual("Thank you for buying with Advantage", self.payment_method.thank_you())
        check_empty = self.pop_up_checkout.get_quantity_after_purchase()
        self.assertIn("Your shopping cart is empty", check_empty)
        x = self.main_page.check_user_orders()
        self.assertEqual(product_name, x.upper())

    def test_9(self):
        self.main_page.click_on_category('tablets')
        self.category_page = Category_Page()  # click on the category page
        self.category_page.scan_products()  # get the list of the products that are in stock from the page
        self.category_page.click_on_product()  # click on some product
        self.product_page1 = Product_Page()  # create instance
        self.product_page1.add_to_cart()  # adding to cart
        product_name = self.product_page1.name
        self.pop_up_checkout = Pop_up_checkout()
        self.pop_up_checkout.click_to_checkout()
        self.order_payment_login = OrderPaymentLogin()
        self.order_payment_login.login_with_exist_user('test_xyz', 'Aasd123')
        self.order_payment_login.click_next()
        self.payment_method = PaymentMethod_Page()
        self.payment_method.pay_with_mastercredit()
        self.assertEqual("Thank you for buying with Advantage", self.payment_method.thank_you())
        check_empty = self.pop_up_checkout.get_quantity_after_purchase()
        self.assertIn("Your shopping cart is empty", check_empty)
        x = self.main_page.check_user_orders()
        self.assertEqual(product_name, x.upper())

    def test_10(self):
        username = 'test_xyz'
        password = 'Aasd123'
        # clicks the login icon above from main and logins
        self.main_page.click_to_login_from_main_page(username, password)  # signs in with this credentials
        account_name = self.main_page.check_login_name()
        self.assertEqual(username, account_name)  # sees if the account shown above the account icon is the same
        time.sleep(2)  # wait between login and logout
        self.main_page.logout_user()  # logs out of the account
        time.sleep(1)  # give time to logout safely
        account_name = self.main_page.check_login_name()  # resigns new account name
        self.assertEqual(account_name, 'out')  # if the user is logged out, the check login name method returns "out"

    def tearDown(self):
        time.sleep(3)
        # Main_Page.get_main_page()
        # self.main_page.driver.close()
        self.main_page.driver.delete_all_cookies()
        self.main_page.driver.refresh()


if __name__ == '__main__':
    unittest.main()






