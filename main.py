from imports import *

def gerar_recibo_pdf(nome_pagador, cpf_pagador, valor, valor_extenso, descricao, forma_pagamento, data, nome_recebedor, cpf_recebedor, arquivo_saida):
    c = canvas.Canvas(arquivo_saida, pagesize=A4)
    width, height = A4
    margem_esquerda = 50
    linha_atual = height - 70

    # 🎨 Inserir logotipo
    caminho_logo = "logo.png"  # ou "logo.jpg", ou path absoluto
    if os.path.exists(caminho_logo):
        try:
            logo = ImageReader(caminho_logo)
            logo_largura = 120
            logo_altura = 60
            c.drawImage(logo, margem_esquerda, height - 80, width=logo_largura, height=logo_altura, mask='auto')
        except Exception as e:
            print(f"Erro ao inserir logotipo: {e}")
    else:
        print("⚠️ Logotipo não encontrado - continuando sem logotipo.")

    # Ajuste na posição do título por causa do logo
    linha_atual -= 40
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, linha_atual, "RECIBO DE PAGAMENTO")
    c.line(margem_esquerda, linha_atual - 10, width - margem_esquerda, linha_atual - 10)

    linha_atual -= 60
    c.setFont("Helvetica", 12)

    c.drawString(margem_esquerda, linha_atual, f"Recebi de: {nome_pagador}")
    linha_atual -= 20
    c.drawString(margem_esquerda, linha_atual, f"CPF/CNPJ do pagador: {cpf_pagador}")

    linha_atual -= 30
    c.drawString(margem_esquerda, linha_atual, f"A quantia de R$ {valor} ({valor_extenso.capitalize()}).")

    linha_atual -= 30
    c.drawString(margem_esquerda, linha_atual, f"Referente a: {descricao}")

    linha_atual -= 20
    c.drawString(margem_esquerda, linha_atual, f"Forma de pagamento: {forma_pagamento}")

    linha_atual -= 30
    c.drawString(margem_esquerda, linha_atual, f"Data do pagamento: {data}")

    linha_atual -= 80
    c.line(margem_esquerda, linha_atual, margem_esquerda + 250, linha_atual)
    linha_atual -= 15
    c.drawString(margem_esquerda, linha_atual, f"Assinatura do recebedor")

    linha_atual -= 40
    c.setFont("Helvetica-Oblique", 11)
    c.drawString(margem_esquerda, linha_atual, f"Nome do recebedor: {nome_recebedor}")
    linha_atual -= 15
    c.drawString(margem_esquerda, linha_atual, f"CPF/CNPJ do recebedor: {cpf_recebedor}")

    c.setFont("Helvetica", 8)
    c.drawCentredString(width / 2, 40, "Documento gerado automaticamente - válido com assinatura")

    c.save()


def gerar_recibo():
    nome_pagador = entry_nome.get()
    cpf_pagador = entry_cpf.get()
    valor = entry_valor.get().replace(" ", "")
    descricao = entry_descricao.get()
    forma_pagamento = entry_forma.get()

    if not (nome_pagador and cpf_pagador and valor and descricao and forma_pagamento):
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    try:
        partes = valor.split(",")
        reais = int(partes[0])
        centavos = int(partes[1]) if len(partes) > 1 else 0

        extenso = num2words(reais, lang="pt-br") + " reais"
        if centavos > 0:
            extenso += f" e {num2words(centavos, lang='pt-br')} centavos"

    except ValueError:
        messagebox.showerror("Erro", "Valor inválido. Use o formato 1234,56")
        return

    data_formatada = datetime.today().strftime("%d/%m/%Y")
    nome_recebedor = "Miguel Galvão Moreira da Silva"
    cpf_recebedor = "111.222.333-44"

    nome_arquivo = f"recibo_{datetime.today().strftime('%Y%m%d_%H%M%S')}.pdf"

    try:
        gerar_recibo_pdf(
            nome_pagador=nome_pagador,
            cpf_pagador=cpf_pagador,
            valor=valor,
            valor_extenso=extenso,
            descricao=descricao,
            forma_pagamento=forma_pagamento,
            data=data_formatada,
            nome_recebedor=nome_recebedor,
            cpf_recebedor=cpf_recebedor,
            arquivo_saida=nome_arquivo
        )
        messagebox.showinfo("Sucesso", f"Recibo salvo como {nome_arquivo}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar recibo:\n{e}")


# Criação da janela
janela = tk.Tk()
janela.title("Gerador de Recibo PDF")
janela.geometry("400x450")
janela.resizable(False, False)

# Estilo simples
tk.Label(janela, text="Nome do Pagador:").pack(pady=5)
entry_nome = tk.Entry(janela, width=50)
entry_nome.pack()

tk.Label(janela, text="CPF/CNPJ do Pagador:").pack(pady=5)
entry_cpf = tk.Entry(janela, width=50)
entry_cpf.pack()

tk.Label(janela, text="Valor (Ex: 1000,50):").pack(pady=5)
entry_valor = tk.Entry(janela, width=20)
entry_valor.pack()

tk.Label(janela, text="Descrição (Referente a):").pack(pady=5)
entry_descricao = tk.Entry(janela, width=50)
entry_descricao.pack()

tk.Label(janela, text="Forma de Pagamento:").pack(pady=5)
entry_forma = tk.Entry(janela, width=30)
entry_forma.pack()

# Botão para gerar
tk.Button(janela, text="Gerar Recibo", width=30, bg='#4CAF50', fg='white', command=gerar_recibo).pack(pady=30)

janela.mainloop()
