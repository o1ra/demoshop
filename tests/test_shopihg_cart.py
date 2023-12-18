import json
import logging
import allure
import requests
from allure_commons._allure import step
from allure_commons.types import AttachmentType
from requests import Response
from selene import browser, have

base_url = 'https://demowebshop.tricentis.com/'


def demowebshop_api_post(url, **kwargs):
    with step("API POST Request"):
        result = requests.post(url=base_url + url, **kwargs)

        allure.attach(body=result.request.url, name="Request url",
                      attachment_type=AttachmentType.TEXT)
        allure.attach(body=json.dumps(result.request.body, indent=4, ensure_ascii=True), name="Request body",
                      attachment_type=AttachmentType.JSON, extension="json")

        allure.attach(body=json.dumps(result.json(), indent=4, ensure_ascii=True), name="Response",
                      attachment_type=AttachmentType.JSON, extension="json")

        logging.info("Request: " + result.request.url)
        if result.request.body:
            logging.info("INFO Request body: " + result.request.body)
        logging.info("Request headers: " + str(result.request.headers))
        logging.info("Response code " + str(result.status_code))
        logging.info("Response: " + result.text)
    return result


def test_add_to_cart_from_catalog_with_api(browser_setup):
    response = demowebshop_api_post('addproducttocart/catalog/22/1/1')
    cookie = response.cookies.get("Nop.customer")

    with step("Set cookie from API"):
        browser.open('/')

        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})

    with step("Open cart"):
        browser.open('/cart')

    with step("Check one item presents"):
        browser.all('.cart-item-row').should(have.size(1))
        browser.all('.cart-item-row').element_by(have.text('Health Book')
                                                 ).element('[name^="itemquantity"]').should(have.value("1"))


def test_add_to_cart_some_desctop_with_ari(browser_setup):
    with (step("Adding to cart a 2 laptop")):
        response = demowebshop_api_post('/addproducttocart/details/31/1',
                                        data={'addtocart_31.EnteredQuantity': 2})

        cookie = response.cookies.get("Nop.customer")

        with step("Set cookie from API"):
            browser.open('/')

            browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})

        with step("Open cart"):
            browser.open('/cart')

        with step("Check one item presents"):
            browser.all('.cart-item-row').should(have.size(1))
            browser.all('.cart-item-row').element_by(have.text('14.1-inch Laptop')
                                                     ).element('[name^="itemquantity"]').should(have.value("2"))


def test_add_phones_and_laptop_with_api(browser_setup):
    with step("Adding to cart laptop"):
        response_1 = demowebshop_api_post('/addproducttocart/catalog/31/1/1')
        cookie_1 = response_1.cookies.get("Nop.customer")

        with step("Adding to cart Smartphone"):
            response_2 = demowebshop_api_post('/addproducttocart/catalog/43/1/1', cookies={"Nop.customer": cookie_1})
            cookie_2 = response_2.cookies.get("Nop.customer")

        with step("Set cookie from API"):
            browser.open('/')

            browser.driver.add_cookie({"name": "Nop.customer", "value": cookie_2})

        with step("Open cart"):
            browser.open('/cart')

        with step("Check one item presents"):
            browser.all('.cart-item-row').should(have.size(2))
            browser.all('.cart-item-row').element_by(have.text('14.1-inch Laptop')
                                                     ).element('[name^="itemquantity"]').should(have.value("1"))
            browser.all('.cart-item-row').element_by(have.text('Smartphone')
                                                     ).element('[name^="itemquantity"]').should(have.value("1"))
