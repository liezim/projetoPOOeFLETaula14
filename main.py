import flet as ft
from datetime import datetime

class Cliente:
    def __init__(self, id: int, nome: str, email: str, telefone: str):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone

class Quarto:
    def __init__(self, numero: int, tipo: str, preco: float, disponivel: bool):
        self.numero = numero
        self.tipo = tipo
        self.preco = preco
        self.disponivel = disponivel

class Reserva:
    def __init__(self, cliente: Cliente, quarto: Quarto, check_in: str, check_out: str, dias: int, total: float, status: str):
        self.cliente = cliente
        self.quarto = quarto
        self.check_in = check_in
        self.check_out = check_out
        self.dias = dias
        self.total = total
        self.status = status

class GerenciadorDeReservas:
    def __init__(self):
        self.clientes = []
        self.quartos = []
        self.reservas = []

    def cadastrar_cliente(self, nome: str, email: str, telefone: str):
        cliente = Cliente(len(self.clientes) + 1, nome, email, telefone)
        self.clientes.append(cliente)
        return cliente

    def cadastrar_quarto(self, numero: int, tipo: str, preco: float, disponivel: bool):
        quarto = Quarto(numero, tipo, preco, disponivel)
        self.quartos.append(quarto)
        return quarto

    def realizar_reserva(self, cliente: Cliente, quarto: Quarto, check_in: str, check_out: str, dias: int, total: float):
        reserva = Reserva(cliente, quarto, check_in, check_out, dias, total, 'Confirmada')
        self.reservas.append(reserva)
        return reserva

    def listar_reservas(self):
        return self.reservas

    def listar_clientes(self):
        return self.clientes

    def cancelar_reserva(self, reserva: Reserva):
        self.reservas.remove(reserva)

    def apagar_cliente(self, cliente: Cliente):
        self.clientes.remove(cliente)

def calcular_dias(check_in: str, check_out: str) -> int:
    try:
        formato = "%d/%m/%Y"
        check_in_date = datetime.strptime(check_in, formato)
        check_out_date = datetime.strptime(check_out, formato)
        delta = check_out_date - check_in_date
        return delta.days
    except ValueError:
        return 0

def formatar_data(data: str) -> str:
    data = data.replace("/", "")
    if len(data) == 8:
        return f"{data[:2]}/{data[2:4]}/{data[4:]}"
    return data

def main(janela: ft.Page):
    janela.bgcolor = '#e3ebee'
    janela.title = "Gerenciamento de Reservas"

    gerenciador = GerenciadorDeReservas()

    gerenciador.cadastrar_quarto(1, 'Single', 100.0, True)
    gerenciador.cadastrar_quarto(2, 'Double', 150.0, True)
    gerenciador.cadastrar_quarto(3, 'Suite', 200.0, True)

    def mostrar_quartos(e):
        quartos_texto = "\n".join([f"{quarto.numero} - {quarto.tipo} - {'Disponível' if quarto.disponivel else 'Indisponível'} - R${quarto.preco}" for quarto in gerenciador.quartos])
        lista_quartos.value = quartos_texto
        janela.update()

    def realizar_reserva(e):
        try:
            cliente_nome = input_nome.value
            cliente_email = input_email.value
            cliente_telefone = input_telefone.value
            quarto_numero = int(input_quarto.value)
            check_in = formatar_data(input_checkin.value)
            check_out = formatar_data(input_checkout.value)

            quarto = None
            for q in gerenciador.quartos:
                if q.numero == quarto_numero:
                    quarto = q
                    break

            if not quarto:
                resultado_reserva.value = f"Erro: O quarto de número {quarto_numero} não encontrado."
                janela.update()
                return

            dias = calcular_dias(check_in, check_out)
            if dias <= 0:
                resultado_reserva.value = "Erro: A data de check-out deve ser posterior à data de check-in."
                janela.update()
                return

            total = dias * quarto.preco
            cliente = gerenciador.cadastrar_cliente(cliente_nome, cliente_email, cliente_telefone)
            reserva = gerenciador.realizar_reserva(cliente, quarto, check_in, check_out, dias, total)
            resultado_reserva.value = f"Reserva confirmada! Quarto {quarto.numero}, {quarto.tipo}, de {check_in} a {check_out}.\nTotal a pagar: R${total:.2f} para {dias} diárias."
            janela.update()

        except ValueError:
            resultado_reserva.value = "Por favor, preencha os campos corretamente."
            janela.update()

    def consultar_reservas(e):
        reservas_texto = []
        for reserva in gerenciador.listar_reservas():
            reserva_texto = f"Cliente: {reserva.cliente.nome} - Quarto {reserva.quarto.numero} ({reserva.quarto.tipo}) - Check-in: {reserva.check_in} - Check-out: {reserva.check_out} - Status: {reserva.status} - Total: R${reserva.total:.2f} "
            cancelar_reserva_botao = ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, r=reserva: cancelar_reserva(r))
            reserva_com_botao = ft.Row([ft.Text(reserva_texto), cancelar_reserva_botao])
            reservas_texto.append(reserva_com_botao)
        lista_reservas.controls = reservas_texto
        janela.update()

    def cancelar_reserva(reserva: Reserva):
        gerenciador.cancelar_reserva(reserva)
        consultar_reservas(None)

    def consultar_clientes(e):
        clientes_texto = []
        for cliente in gerenciador.listar_clientes():
            cliente_texto = f"Cliente {cliente.id}: {cliente.nome} - {cliente.email} - {cliente.telefone}"
            apagar_cliente_botao = ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, c=cliente: apagar_cliente(c))
            cliente_com_botao = ft.Row([ft.Text(cliente_texto), apagar_cliente_botao])
            clientes_texto.append(cliente_com_botao)
        lista_clientes.controls = clientes_texto
        janela.update()

    def apagar_cliente(cliente: Cliente):
        gerenciador.apagar_cliente(cliente)
        consultar_clientes(None)

    lista_quartos = ft.Text(value="")
    lista_reservas = ft.Column()
    lista_clientes = ft.Column()

    botao_mostrar_quartos = ft.ElevatedButton(text="Tipo de Quartos", on_click=mostrar_quartos)
    botao_reservar = ft.ElevatedButton(text="Realizar Reserva", on_click=realizar_reserva)
    botao_consultar_reservas = ft.ElevatedButton(text="Consultar Reservas", on_click=consultar_reservas)
    botao_consultar_clientes = ft.ElevatedButton(text="Consultar Clientes", on_click=consultar_clientes)

    input_nome = ft.TextField(label="Nome do Cliente")
    input_email = ft.TextField(label="E-mail do Cliente")
    input_telefone = ft.TextField(label="Telefone do Cliente")
    input_quarto = ft.TextField(label="Tipo do Quarto (1,2,3)")
    input_checkin = ft.TextField(label="Data de Check-in (DD/MM/AAAA)")
    input_checkout = ft.TextField(label="Data de Check-out (DD/MM/AAAA)")
    resultado_reserva = ft.Text(value="")

    janela.add(
        botao_mostrar_quartos,
        lista_quartos,
        input_nome,
        input_email,
        input_telefone,
        input_checkin,
        input_checkout,
        botao_reservar,
        input_quarto,
        botao_consultar_reservas,
        lista_reservas,
        botao_consultar_clientes,
        lista_clientes,
        resultado_reserva
    )

ft.app(target=main)
