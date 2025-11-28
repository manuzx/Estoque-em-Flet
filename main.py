import flet as ft
from conexao import validar_login
import sistema

def main(page: ft.Page):
    page.title="Estoque SAEP - Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    email_caixa = ft.TextField(label="Email", width=300)
    senha_caixa = ft.TextField(label="Senha", width=300, password=True)

    def btn_acesso(e):
        email = email_caixa.value
        senha = senha_caixa.value

        usuario = validar_login(email, senha)
        
        if usuario:
            sistema.menu_principal(page, usuario)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Dados inválidos! Tente novamente."),bgcolor = 'red')

            page.snack_bar.open = True
            page.update()



    btn_entrar = ft.ElevatedButton(text="Entrar", on_click=btn_acesso,width=300)

    page.add(
        ft.Text("Estoque SAEP", size=30, weight="bold"),
        email_caixa,
        senha_caixa,
        btn_entrar
    )

ft.app(target=main)

