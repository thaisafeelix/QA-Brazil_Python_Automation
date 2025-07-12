import time

from pages import UrbanRoutesPage
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from helpers import retrieve_phone_code
import data
import helpers

class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = Chrome()
        cls.driver.implicitly_wait(5)

        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Conectado ao servidor Urban Routes")
        else:
            print("Não é possível conectar ao Urban Routes. Verifique se o servidor está ligado e em execução.")

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_to_location(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert routes_page.get_from_location_value() == data.ADDRESS_FROM
        assert routes_page.get_to_location_value() == data.ADDRESS_TO

    def test_select_plan(self):
        print("Seleção de plano...")
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        WebDriverWait(self.driver, timeout=1).until(lambda d: True)
        routes_page.click_taxi_option()
        WebDriverWait(self.driver, timeout=1).until(lambda d: True)
        routes_page.click_comfort_icon()
        WebDriverWait(self.driver, timeout=1).until(lambda d: True)
        assert routes_page.click_comfort_active()

    def test_fill_phone_number(self):
        print("Preenchimento do número de telefone...")
        self.driver.get(data.URBAN_ROUTES_URL)
        route_page = UrbanRoutesPage(self.driver)
        route_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        WebDriverWait(self.driver, timeout=1).until(lambda d: True)
        phone_number = retrieve_phone_code() + "12312312312"
        route_page.fill_phone_number(phone_number)
        WebDriverWait(self.driver, timeout=1).until(lambda d: True)
        filled_number = route_page.get_phone_number_value()
        assert filled_number == phone_number

    def test_fill_card(self):
        print("Preenchimento dos dados do cartão...")
        self.driver.get(data.URBAN_ROUTES_URL)
        route_page = UrbanRoutesPage(self.driver)
        route_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        route_page.click_taxi_option()
        route_page.click_comfort_icon()
        route_page.click_add_cartao(data.CARD_NUMBER, data.CARD_CODE)
        assert "Cartão" in route_page.confirm_cartao()

    def test_comment_for_driver(self):
        print("Adição de comentário para o motorista...")
        self.driver.get(data.URBAN_ROUTES_URL)
        route_page = UrbanRoutesPage(self.driver)
        route_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        WebDriverWait(self.driver, timeout=1).until(lambda d: True)
        comment = "Por favor, dirija com cuidado."
        route_page.add_driver_comment(comment)
        WebDriverWait(self.driver, timeout=1).until(lambda d: True)
        filled_comment = route_page.get_driver_comment()
        assert filled_comment == comment

    def test_order_blanket_and_handkerchiefs(self):
        print("Solicitação de cobertor e lenço...")
        self.driver.get(data.URBAN_ROUTES_URL)
        route_page = UrbanRoutesPage(self.driver)
        route_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        WebDriverWait(self.driver, timeout=1).until(lambda d: True)
        route_page.select_blanket_option()
        route_page.select_handkerchief_option()
        WebDriverWait(self.driver, timeout=1).until(lambda d: True)
        assert route_page.is_blanket_selected()
        assert route_page.is_handkerchief_selected()

    def test_order_2_ice_creams(self):
        print("Pedido de 2 sorvetes")
        self.driver.get(data.URBAN_ROUTES_URL)
        route_page = UrbanRoutesPage(self.driver)
        route_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        route_page.click_taxi_option()
        route_page.click_comfort_icon()
        for _ in range(2):
            routes_page.add_ice_cream()
        assert int(route_page.qnt_sorvete()) == 2

    def test_car_search_model_appears(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.click_taxi_option()
        routes_page.click_comfort_icon()
        routes_page.click_number_text(data.PHONE_NUMBER)
        routes_page.click_add_cartao(data.CARD_NUMBER, data.CARD_CODE)
        routes_page.add_comentario(data.MESSAGE_FOR_DRIVER)
        routes_page.call_taxi()
        assert "Buscar carro" in routes_page.pop_up_show()
        time.sleep(10)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()