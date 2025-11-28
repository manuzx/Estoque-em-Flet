import flet as ft
from conexao import validar_login

def main(page: ft.Page):
    page.title="Estoque SAEP - Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    email_caixa = ft.TextField(label="Email", width=300)
    senha_caixa = ft.TextField(label="Senha", width=300, password=True)

    def btn_acesso(e):
        pass
    #volto aqui depois

    btn_entrar = ft.ElevatedButton(text="Entrar", on_click=btn_acesso,width=300)

    page.add(
        ft.Text("Estoque SAEP", size=30, weight="bold"),
        email_caixa,
        senha_caixa,
        btn_entrar
    )

ft.app(target=main)