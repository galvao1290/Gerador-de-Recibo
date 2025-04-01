from imports import *

def wrap_text(text, max_width, canvas, font_name='Helvetica', font_size=12):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        if canvas.stringWidth(current_line + " " + word, font_name, font_size) <= max_width:
            current_line += " " + word
        else:
            lines.append(current_line.strip())
            current_line = word
    lines.append(current_line.strip())
    return lines

def gerar_recibo_pdf(nome_pagador, cpf_pagador, valor, valor_extenso, descricao, forma_pagamento, data, nome_recebedor, cpf_recebedor, arquivo_saida):
    c = canvas.Canvas(arquivo_saida, pagesize=A4)
    width, height = A4
    margem_esquerda = 50
    margem_direita = 50
    linha_atual = height - 70
    max_width = width - margem_esquerda - margem_direita

    # Inserir logotipo
    caminho_logo = "logo.png" 
    if os.path.exists(caminho_logo):
        try:
            logo = ImageReader(caminho_logo)
            logo_largura = 120
            logo_altura = 60
            c.drawImage(logo, margem_esquerda, height - 80, width=logo_largura, height=logo_altura, mask='auto')
        except Exception as e:
            print(f"Erro ao inserir logotipo: {e}")
    else:
        print("Logotipo não encontrado - continuando sem logotipo.")


    linha_atual -= 40
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, linha_atual, "RECIBO DE PAGAMENTO")
    c.line(margem_esquerda, linha_atual - 10, width - margem_direita, linha_atual - 10)

    linha_atual -= 60
    c.setFont("Helvetica", 12)


    def desenhar_texto_negrito(label, texto, y):
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margem_esquerda, y, label)
        c.setFont("Helvetica", 12)
        
        wrapped_text = wrap_text(texto, max_width - 150, c)
        for i, line in enumerate(wrapped_text):
            c.drawString(margem_esquerda + 150, y - (i * 14), line)
        return y - (len(wrapped_text) * 14)

    linha_atual = desenhar_texto_negrito("Recebi de:", nome_pagador, linha_atual)
    linha_atual -= 20
    linha_atual = desenhar_texto_negrito("CPF/CNPJ do pagador:", cpf_pagador, linha_atual)

    linha_atual -= 30
    linha_atual = desenhar_texto_negrito("A quantia de R$:", f"{valor} ({valor_extenso.capitalize()})", linha_atual)

    linha_atual -= 30
    linha_atual = desenhar_texto_negrito("Referente a:", descricao, linha_atual)

    linha_atual -= 20
    linha_atual = desenhar_texto_negrito("Forma de pagamento:", forma_pagamento, linha_atual)

    linha_atual -= 30
    linha_atual = desenhar_texto_negrito("Data do pagamento:", data, linha_atual)

    linha_atual -= 80
    c.line(margem_esquerda, linha_atual, margem_esquerda + 250, linha_atual)
    linha_atual -= 15
    c.drawString(margem_esquerda, linha_atual, "Assinatura do recebedor")

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



janela = tk.Tk()
janela.title("Gerador de Recibo PDF")
janela.geometry("400x450")
janela.resizable(False, False)


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

tk.Button(janela, text="Gerar Recibo", width=30, bg='#4CAF50', fg='white', command=gerar_recibo).pack(pady=30)

janela.mainloop()
