import flet as ft
import conexao as db 

def menu_principal(page:ft.Page,usuario):
    page.clean()

    def ir_produto(e):
        tela_produtos(page, usuario)

    def ir_estoque(e):
        tela_produtos(page, usuario)

    def logout(e):
        page.window.close()

    header = ft.Row([
        ft.Text(f'Olá,{usuario[1]}', size=20, weight='bold'),
        ft.ElevatedButton('Sair', on_click=logout, bgcolor=ft.Colors.
        RED_400, color='white')
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    botoes = ft.Column([
        ft.ElevatedButton('Cadastro de Produto',
        on_click=ir_produto, height=60, width=300),
        ft.ElevatedButton('Gestão de Estoque', on_click=ir_estoque,
        height=60, width=300)], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
    
    page.add(header, ft.Divider(), ft.Container(content=botoes,padding=50, alignment=ft.alignment.center))
     
def tela_produtos(page: ft.Page, usuario):
    page.clean()

    nome = ft.TextField(label='Nome do Produto')
    cat = ft.TextField(label='Categoria')
    lote = ft.TextField(lote='Lote')
    validade = ft.TextField(label='validade (AAAA-MM-DD)')
    qtd = ft.TextField(label='qtd inicial', value='0', keyboard_type="number")
    minimo = ft.TextField(label='Nome do Produto', value='5', keyboard_type="number")

    tabela = ft.DataTable(columns=[
        ft.DataColumn(ft.Text('ID')),
        ft.DataColumn(ft.Text('Nome')),
        ft  .DataColumn(ft.Text('Lote')),
        ft.DataColumn(ft.Text('Qtd')),
        ft.DataColumn(ft.Text('Ações')),
    ], rows=[])

    def carregar_dados(e=None):
        tabela.rows.clear()
        produtos = db.listar_produtos()
        for p in produtos:
            btn_edl = ft.IconButton(icon=ft.Icons.DELETE, icon_color='red',data=p[0], on_click=deletar_item)
      


        tabela.rows.append(
            ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(p[0]))),
                    ft.DataCell(ft.Text(p[1])),
                    ft.DataCell(ft.Text(p[5])),
                    ft.DataCell(ft.Text(str(p[2]))),
                    ft.DataCell(btn_edl)
                ])
            ) 

        page.update()

    def salvar(e):
        if not nome.value or not lote.value:
            page.snack_bar = ft.SnackBar(ft.Text('Preencha os campos obrigatórios!'))
            page.snack_bar.open = True

        db.salvar_produto(nome.value, lote.value, validade.value, int(qtd.value), int(minimo.value))
        page.snack_bar = ft.SnackBar(ft.Text('Produto salvo com sucesso!'), bgcolor='green')
        page.snack_bar.open = True

        nome.value = ''
        lote.value = ''
        carregar_dados()

    def deletar_item(e):
        db.deletar_produto(e.control.data)
        carregar_dados()      

    def voltar(e):
        menu_principal(page, usuario)

    page.add(
        ft.Row([ft.Text('Cadastro de Produtos', size=25), ft.ElevatedButton('Voltar', on_click=voltar)]),
        ft.Column([nome, cat, lote, validade, qtd, minimo], scroll='True', height=300),
        ft.ElevatedButton('Salvar Produto', on_click=salvar),
        ft.Divider(),
        ft.Text('Lista de Produtos', size=20),
        ft.Container([tabela], scroll='True', height=200)
    )

    carregar_dados()

def taela_estoque(page: ft.Page, usuario):
    page.clean()
    
    produtos = db.listar_produtos()
    opcoes = [ft.dropdown.Option(key=str(p[0]), text=f'{p[1]} (Atual: {p[2]})') for p in produtos]

    select_prod = ft.Dropdown(label='Selecione o Produto', options=opcoes)
    tipo_mov = ft.RadioGroup(content=ft.Row([
        ft.Radio(value='Entrada', label='Entrada'),
        ft.Radio(value='Saída', label='Saída')
    ]))

    qtd_mov = ft.TextField(label='Quantidade', keyboard_type='number')

    def confirmar(e):
        if not select_prod.value or not qtd_mov.value or not tipo_mov.value:
            return
        
        alerta, nome_prod = db.registrar_movimento(
            int(select_prod.value),
            int(qtd_mov.value),
            tipo_mov.value,
            usuario[0]
        )

        msg = 'Movimento registrado com sucesso!'
        cor = "green"

        if alerta:
            msg = f"ALERTA: {nome_prod} está abaixo do estoque mínimo!"
            cor = "red"

        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=cor)
        page.snack_bar.open = True

        taela_estoque(page, usuario)

        page.add(
            ft.Text('Gestão de Estoque', size=25),select_prod, ft.Text('Tipo:'), tipo_mov, qtd_mov,
            ft.ElevatedButton('Confirmar', on_click=confirmar),
            ft.ElevatedButton('Voltar', on_click=lambda e: menu_principal(page, usuario))
        )