import data
import helpers


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Conectado ao servidor Urban Routes")
        else:
            print("Não foi possível conectar ao Urban Routes. Verifique se o servidor está ligado e ainda em execução.")

    def test_set_route(self):
        print("Função criada para definir a rota")
        stations = data.get_stations()
        origin = "S1"
        destination = "S8"
        route = helpers.set_route(origin, destination)
        assert destination in route, f"A estação de destino {destination} não foi encontrada na rota."
        print("Rota definida com sucesso:", route)

    def test_select_plan(self):
        print("Função criada para selecionar o plano")
        selected_plan = helpers.select_plan("premium")
        assert selected_plan == "premium"
        print("Plano selecionado com sucesso:", selected_plan)

    def test_fill_phone_number(self):
        print("Função criada para preencher número de telefone")
        number = "11999999999"
        valid = helpers.fill_phone_number(number)
        assert valid
        print("Número de telefone preenchido com sucesso:", number)

    def test_fill_card(self):
        print("Função criada para preencher dados do cartão")
        card_info = {
            "number": "4111111111111111",
            "expiration": "12/26",
            "cvv": "123"
        }
        valid = helpers.fill_card(card_info)
        assert valid
        print("Cartão preenchido com sucesso.")

    def test_comment_for_driver(self):
        print("Função criada para adicionar comentário para o motorista")
        comment = "Motorista muito educado e pontual!"
        success = helpers.comment_for_driver(comment)
        assert success
        print("Comentário enviado com sucesso.")

    def test_order_blanket_and_handkerchiefs(self):
        print("Função criada para solicitar cobertor e lenço")
        items = ["cobertor", "lenço"]
        order = helpers.order_items(items)
        assert "cobertor" in order and "lenço" in order
        print("Pedido feito com sucesso:", order)

    def test_order_2_ice_creams(self):
        print("Função criada para definir o pedido do sorvete")
        quantity = 2
        order = helpers.order_item("sorvete", quantity)

        if order.get("sorvete") == 2:
            print("Pedido de sorvetes realizado com sucesso:", order)
        else:
            print("Erro: Quantidade de sorvetes incorreta.")
            print("Pedido retornado:", order)
            assert False, "A quantidade de sorvetes no pedido não é igual a 2"

    def test_car_search_model_appears(self):
        print("Função criada para verificar se modelo do carro aparece na busca")
        car_model = "Toyota Corolla"
        found_models = helpers.search_cars("Toyota")
        assert car_model in found_models
        print("Modelo encontrado na busca:", car_model)