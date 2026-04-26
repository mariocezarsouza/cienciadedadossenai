# ============================================================
#  SIMULADOR DE ARMAZENAGEM E PROTEÇÃO DE EMBALAGENS  v3
#  Doceria Famoso | SENAI Euvaldo Lodi – Contagem (MG)
#  UCE I – Tecnólogo em Ciência de Dados
# ============================================================
#
#  NOVIDADE desta versão:
#  O usuário informa o VALOR UNITÁRIO e a QUANTIDADE real
#  de cada solução. O custo total é calculado automaticamente.
#
#  ESTRUTURA DO PROGRAMA:
#  1. coletar_dados_gerais()    → área, caixa, perda por caixa
#  2. coletar_dados_solucoes()  → valor unit. + qtd. + % redução
#  3. calcular_ocupacao()       → caixas por camada, total, perda
#  4. calcular_custo_solucao()  → custo total de cada solução
#  5. analisar_solucoes()       → economia líq., ROI, melhor opção
#  6. imprimir_relatorio()      → exibe tudo formatado no terminal
#  7. main()                    → loop de controle do programa
# ============================================================


def coletar_dados_gerais():
    """
    Coleta os dados físicos do armazém e da caixa.
    Retorna um dicionário com todos os valores validados.
    """
    print("\n" + "=" * 82)
    print("   SIMULADOR DE ARMAZENAGEM E PROTEÇÃO DE EMBALAGENS – DOCERIA FAMOSO")
    print("   FACULDADE SENAI – Contagem (MG)")
    print("   UCE I – Tecnólogo em Ciência de Dados")
    print("   Grupo de trabalho: Daniel - Felipe - Fernando - Marcos - Mário - Matheus")
    print("   Orientadora: Profa. Dra. Michele Cândida Carvalho de Oliveira")
    print("=" * 82)
    print("\n[ETAPA 1 de 2] DADOS DO ARMAZÉM E DAS CAIXAS\n")

    dados = {
        "area_total":    float(input("  Área total disponível (m²): ")),
        "larg_cx":       float(input("  Largura da caixa (m): ")),
        "comp_cx":       float(input("  Comprimento da caixa (m): ")),
        "alt_cx":        float(input("  Altura da caixa (m): ")),
        "pilha":         int(input("  Nível de empilhamento (camadas): ")),
        "valor_perdida": float(input("  Valor médio por caixa danificada (R$): ")),
    }

    # Validação: todos os campos devem ser positivos
    for chave, valor in dados.items():
        if valor <= 0:
            raise ValueError(f"O campo '{chave}' deve ser maior que zero.")

    return dados


def coletar_dados_solucoes(total_caixas):
    """
    Coleta os dados específicos de cada solução de proteção.

    Para as CANTONEIRAS, o custo é calculado por unidade × quantidade
    por caixa × total de caixas — porque cada caixa recebe cantoneiras.

    Para ESTANTES e DIVISÓRIAS, o custo é calculado por unidade ×
    quantidade total — porque são instaladas no espaço, não por caixa.

    Parâmetro:
        total_caixas (int): quantidade total de caixas no armazém,
                            necessária para calcular o custo das cantoneiras.

    Retorna uma lista de 3 dicionários, um por solução.
    """
    print("\n[ETAPA 2 de 2] CUSTOS REAIS DE CADA SOLUÇÃO\n")

    # --- Solução 1: Cantoneiras ---
    print("  -- Cantoneiras V-Board --")
    v_cant  = float(input("     Valor unitário da cantoneira (R$): "))
    q_cant  = int(input(f"     Quantidade por caixa (padrão 4): "))
    r_cant  = float(input("     Redução de danos estimada (%): "))

    # Custo total = valor_unit × qtd_por_caixa × total_caixas
    custo_cant = v_cant * q_cant * total_caixas
    qtd_total_cant = q_cant * total_caixas

    # --- Solução 2: Estantes ---
    print("\n  -- Estantes de Aço --")
    v_est   = float(input("     Valor unitário da estante (R$): "))
    q_est   = int(input("     Quantidade de estantes necessárias: "))
    r_est   = float(input("     Redução de danos estimada (%): "))

    custo_est = v_est * q_est

    # --- Solução 3: Divisórias ---
    print("\n  -- Divisórias Modulares --")
    v_div   = float(input("     Valor unitário da divisória (R$): "))
    q_div   = int(input("     Quantidade de divisórias necessárias: "))
    r_div   = float(input("     Redução de danos estimada (%): "))

    custo_div = v_div * q_div

    # Validações básicas
    for nome, val in [("valor cantoneira", v_cant), ("qtd cantoneira", q_cant),
                      ("redução cant.", r_cant), ("valor estante", v_est),
                      ("qtd estante", q_est), ("redução est.", r_est),
                      ("valor divisória", v_div), ("qtd divisória", q_div),
                      ("redução div.", r_div)]:
        if val <= 0:
            raise ValueError(f"O campo '{nome}' deve ser maior que zero.")
    for nome, val in [("redução cant.", r_cant), ("redução est.", r_est), ("redução div.", r_div)]:
        if val > 100:
            raise ValueError(f"'{nome}' não pode ultrapassar 100%.")

    return [
        {
            "nome":     "Cantoneiras V-Board",
            "qtd":      qtd_total_cant,
            "v_unit":   v_cant,
            "custo":    custo_cant,
            "reducao":  r_cant,
            "detalhe":  f"{qtd_total_cant} unid. x R$ {v_cant:.2f}",
        },
        {
            "nome":     "Estantes de Aço",
            "qtd":      q_est,
            "v_unit":   v_est,
            "custo":    custo_est,
            "reducao":  r_est,
            "detalhe":  f"{q_est} estantes x R$ {v_est:.2f}",
        },
        {
            "nome":     "Divisórias Modulares",
            "qtd":      q_div,
            "v_unit":   v_div,
            "custo":    custo_div,
            "reducao":  r_div,
            "detalhe":  f"{q_div} divisórias x R$ {v_div:.2f}",
        },
    ]


def calcular_ocupacao(d):
    """
    Calcula a capacidade física do armazém.
    - area_caixa    : espaço que cada caixa ocupa no chão
    - por_camada    : quantas caixas cabem em uma camada (divisão inteira)
    - total_caixas  : por_camada × número de camadas
    - perda_maxima  : perda financeira se 100% das caixas forem danificadas
    """
    area_cx = d["larg_cx"] * d["comp_cx"]
    por_camada = int(d["area_total"] // area_cx)
    total = por_camada * d["pilha"]
    perda = total * d["valor_perdida"]
    return {
        "area_cx":    area_cx,
        "por_camada": por_camada,
        "total":      total,
        "perda":      perda,
    }


def analisar_solucoes(solucoes, perda_total):
    """
    Enriquece cada solução com:
    - perda_evitada  : quanto da perda total esta solução elimina
    - econ_liquida   : perda_evitada - custo_da_solução
    - roi_percent    : retorno sobre o investimento em %
    - cb_ratio       : custo por ponto percentual de proteção (menor = melhor)

    Identifica a melhor solução pelo menor cb_ratio.
    """
    for s in solucoes:
        s["perda_evitada"] = perda_total * s["reducao"] / 100
        s["econ_liquida"]  = s["perda_evitada"] - s["custo"]
        s["roi"]           = (s["econ_liquida"] / s["custo"]) * 100 if s["custo"] > 0 else 0
        s["cb_ratio"]      = s["custo"] / s["reducao"]   # custo/eficácia

    melhor = min(solucoes, key=lambda x: x["cb_ratio"])
    return solucoes, melhor


def barra_ascii(valor, maximo, largura=40):
    """
    Gera uma barra ASCII proporcional.
    Parâmetros:
        valor   : valor atual
        maximo  : valor máximo da escala
        largura : número total de caracteres da barra
    """
    if maximo == 0:
        return " " * largura
    blocos = int((valor / maximo) * largura)
    return "█" * blocos + " " * (largura - blocos)


def imprimir_relatorio(d, ocup, solucoes, melhor):
    """
    Exibe o relatório técnico completo no terminal, em seções:
    1. Capacidade física
    2. Risco financeiro
    3. Comparativo detalhado (tabela)
    4. Gráficos ASCII de custo e proteção
    5. Conclusão com ROI e recomendação
    """
    sep = "=" * 82
    lin = "-" * 82

    print(f"\n{sep}")
    print("  RELATÓRIO TÉCNICO DE ARMAZENAGEM")
    print(sep)

    # --- 1. Capacidade ---
    print("\n  [1] CAPACIDADE FÍSICA\n")
    print(f"  Área total           : {d['area_total']:.2f} m²")
    print(f"  Área por caixa       : {ocup['area_cx']:.4f} m²")
    print(f"  Caixas por camada    : {ocup['por_camada']}")
    print(f"  Camadas empilhadas   : {d['pilha']}")
    print(f"  Total de caixas      : {ocup['total']}")

    # --- 2. Risco ---
    print("\n  [2] RISCO FINANCEIRO SEM PROTEÇÃO\n")
    print(f"  Valor por caixa dand.: R$ {d['valor_perdida']:,.2f}")
    print(f"  Perda potencial total: R$ {ocup['perda']:,.2f}")

    # --- 3. Tabela comparativa ---
    print(f"\n  [3] COMPARATIVO DETALHADO\n")
    header = f"  {'Solução':<24} {'Qtd':>6} {'Custo Total':>13} {'Prot.':>7} {'Econ.Líq.':>13} {'ROI':>7}"
    print(header)
    print(f"  {lin}")

    max_custo = max(s["custo"] for s in solucoes)

    for s in solucoes:
        marcador = " ◄" if s["nome"] == melhor["nome"] else "  "
        print(
            f"  {s['nome']:<24} "
            f"{s['qtd']:>6,} "
            f"R$ {s['custo']:>9,.2f} "
            f"{s['reducao']:>6.0f}% "
            f"R$ {s['econ_liquida']:>9,.2f} "
            f"{s['roi']:>6.0f}%"
            f"{marcador}"
        )

    # --- 4. Gráficos ASCII ---
    print(f"\n  [4] CUSTO TOTAL (R$)  — barra proporcional ao maior valor\n")
    print(f"  {lin}")
    for s in solucoes:
        barra = barra_ascii(s["custo"], max_custo, largura=36)
        print(f"  {s['nome']:<22} |{barra}| R$ {s['custo']:,.2f}")
    print(f"  {lin}")

    max_prot = 100
    print(f"\n  [4b] PROTEÇÃO (%)  — barra proporcional a 100%\n")
    print(f"  {lin}")
    for s in solucoes:
        barra = barra_ascii(s["reducao"], max_prot, largura=36)
        print(f"  {s['nome']:<22} |{barra}| {s['reducao']:.0f}%")
    print(f"  {lin}")

    # --- 5. Conclusão ---
    print(f"\n{sep}")
    print("  CONCLUSÃO TÉCNICA")
    print(sep)
    print(f"\n  Solução recomendada : {melhor['nome']}")
    print(f"  Base de cálculo     : {melhor['detalhe']}")
    print(f"  Custo de implantação: R$ {melhor['custo']:,.2f}")
    print(f"  Proteção esperada   : {melhor['reducao']:.0f}%")
    print(f"  Perda evitada       : R$ {melhor['perda_evitada']:,.2f}")
    print(f"  Economia líquida    : R$ {melhor['econ_liquida']:,.2f}")
    print(f"  ROI estimado        : {melhor['roi']:.0f}%")
    print(f"\n{sep}\n")


def main():
    """
    Loop principal do programa.
    Controla o fluxo: coleta → calcula → exibe → repete ou encerra.
    """
    print("\n  Bem-vindo ao Simulador de Armazenagem – Doceria Famoso")

    while True:
        try:
            # Passo 1: dados gerais (armazém + caixas)
            dados = coletar_dados_gerais()

            # Passo 2: ocupação física (necessário antes de coletar soluções,
            #          pois a quantidade de cantoneiras depende do total de caixas)
            ocupacao = calcular_ocupacao(dados)

            print(f"\n  [INFO] No espaço de {dados['area_total']:.1f} m² cabem "
                  f"{ocupacao['por_camada']} caixas por camada.")
            print(f"  [INFO] Total monitorado: {ocupacao['total']} caixas.")
            print(f"  [INFO] Perda potencial sem proteção: R$ {ocupacao['perda']:,.2f}\n")

            # Passo 3: dados de cada solução (com total de caixas disponível)
            solucoes = coletar_dados_solucoes(ocupacao["total"])

            # Passo 4: análise de custo-benefício
            solucoes, melhor = analisar_solucoes(solucoes, ocupacao["perda"])

            # Passo 5: relatório final
            imprimir_relatorio(dados, ocupacao, solucoes, melhor)

        except ValueError as e:
            print(f"\n  [ERRO] {e}")
            print("  Use ponto (.) para decimais. Ex.: 1.50 em vez de 1,50\n")

        # Controle de fluxo (executado mesmo após erros)
        print("=" * 82)
        cmd = input("  [1] Novo cálculo   [0] Sair: ").strip()

        if cmd == "0":
            print("\n  Encerrando. Relatório finalizado para o SENAI.\n")
            break
        elif cmd == "1":
            continue
        else:
            print("\n  Comando inválido. Reiniciando...\n")
            continue


if __name__ == "__main__":
    main()
