import pandas as pd
import streamlit as st
import plotly.express as px

# Carregar os dados da planilha
# Supondo que seus dados estejam em um arquivo CSV chamado 'seu_arquivo.csv'
try:
    df = pd.read_csv('data_com_diferenca33.csv')
except FileNotFoundError:
    st.error("Arquivo 'seu_arquivo.csv' não encontrado. Certifique-se de que o arquivo está no mesmo diretório do script.")
    st.stop()

# Calcular o valor do desconto


# Título do Dashboard
st.title("Dashboard Interativo de Produtos para Análise de Cupons")

# Sidebar para filtros
st.sidebar.header("Filtros")

# Filtro por marca (multiseleção)
try:
    marcas_unicas = sorted([str(marca) for marca in df['brand'].dropna().unique()])
    selected_brands = st.sidebar.multiselect("Marca:", marcas_unicas, default=marcas_unicas, key="brand_filter")
    df_filtered = df[df['brand'].isin(selected_brands)]
except KeyError:
    st.error("A coluna 'brand' não foi encontrada no arquivo CSV.")
    st.stop()

# Filtro por vendedor (multiseleção)
try:
    vendedores_unicos = sorted(
        df_filtered['seller'].fillna('vendedor não identificado').astype(str).unique()
    )
    selected_sellers = st.sidebar.multiselect("Vendedor:", vendedores_unicos, default=vendedores_unicos, key="seller_filter")
    df_filtered = df_filtered[df_filtered['seller'].isin(selected_sellers)]
except KeyError:
    st.error("A coluna 'seller' não foi encontrada no DataFrame após o filtro de marcas.")
    st.stop()

# Filtro por frete grátis (multiseleção)
try:
    frete_options = sorted(df_filtered['frete_gratis'].unique())
    selected_frete = st.sidebar.multiselect("Frete Grátis:", frete_options, default=frete_options, key="frete_gratis_filter")
    df_filtered = df_filtered[df_filtered['frete_gratis'].isin(selected_frete)]
except KeyError:
    st.error("A coluna 'frete_gratis' não foi encontrada no DataFrame após os filtros anteriores.")
    st.stop()

# Filtro por full (multiseleção)
try:
    full_options = sorted(df_filtered['full'].unique())
    selected_full = st.sidebar.multiselect("Full:", full_options, default=full_options, key="full_filter")
    df_filtered = df_filtered[df_filtered['full'].isin(selected_full)]
except KeyError:
    st.error("A coluna 'full' não foi encontrada no DataFrame após os filtros anteriores.")
    st.stop()

# Filtro por entrega rápida (multiseleção)
try:
    entrega_rapida_options = sorted(df_filtered['entrega_rapida'].unique())
    selected_entrega_rapida = st.sidebar.multiselect("Entrega Rápida:", entrega_rapida_options, default=entrega_rapida_options, key="entrega_rapida_filter")
    df_filtered = df_filtered[df_filtered['entrega_rapida'].isin(selected_entrega_rapida)]
except KeyError:
    st.error("A coluna 'entrega_rapida' não foi encontrada no DataFrame após os filtros anteriores.")
    st.stop()

# Filtro por entrega mesmo dia (multiseleção)
try:
    entrega_mesmo_dia_options = sorted(df_filtered['entrega_mesmo_dia'].unique())
    selected_entrega_mesmo_dia = st.sidebar.multiselect("Entrega Mesmo Dia:", entrega_mesmo_dia_options, default=entrega_mesmo_dia_options, key="entrega_mesmo_dia_filter")
    df_filtered = df_filtered[df_filtered['entrega_mesmo_dia'].isin(selected_entrega_mesmo_dia)]
except KeyError:
    st.error("A coluna 'entrega_mesmo_dia' não foi encontrada no DataFrame após os filtros anteriores.")
    st.stop()

# Filtro por percentual de desconto
try:
    percentuais_unicos = sorted(df_filtered['percentual_desconto'].unique())
    selected_percentuais = st.sidebar.multiselect("Percentual de Desconto:", percentuais_unicos, default=percentuais_unicos, key="percentual_desconto_filter")
    df_filtered = df_filtered[df_filtered['percentual_desconto'].isin(selected_percentuais)]
except KeyError:
    st.error("A coluna 'percentual_desconto' não foi encontrada no DataFrame após os filtros anteriores.")
    st.stop()

# --- Visualizações Relevantes para Cupons Afiliados ---


try:
    st.subheader("Distribuição de Preços Novos")
    fig_price = px.histogram(df_filtered, x='price_new', nbins=20, title='Distribuição de Preços Novos')
    st.plotly_chart(fig_price)
    st.info(
        "Use esta distribuição para entender a faixa de preços dos produtos. Foque em cupons para produtos dentro das faixas de preço mais populares ou em descontos significativos em produtos de maior valor.")
except KeyError:
    st.error("A coluna 'price_new' não foi encontrada no DataFrame após os filtros.")

    try:
        st.subheader("Avaliação vs. Preço")
        df_filtered = df_filtered[df_filtered['number_rating'].notna()]
        fig_rating_price = px.scatter(df_filtered, x='price_new', y='rating', size='number_rating', color='brand',
                                      hover_data=['name', 'seller', 'frete_gratis', 'full', 'entrega_rapida',
                                                  'entrega_mesmo_dia'],
                                      title='Avaliação vs. Preço (Tamanho por Número de Avaliações)')
        st.plotly_chart(fig_rating_price)
        st.info(
            "Analise se produtos mais caros tendem a ter melhores avaliações. Divulgue cupons para produtos bem avaliados, independentemente do preço, ou destaque descontos em produtos de alta qualidade para torná-los mais acessíveis.")
    except KeyError as e:
        st.error(f"Uma ou mais colunas necessárias para o gráfico 'Avaliação vs. Preço' não foram encontradas: {e}")

    try:
        st.subheader("Média de Desconto por Marca (Top 10)")
        brand_avg_discount = df_filtered.groupby('brand')['desconto'].mean().sort_values(ascending=False).head(
            10).reset_index()
        fig_discount_brand = px.bar(brand_avg_discount, x='brand', y='desconto',
                                    title='Top 10 Marcas por Média de Desconto')
        st.plotly_chart(fig_discount_brand)
        st.info(
            "Identifique as marcas que oferecem os maiores descontos médios. Concentre seus esforços em encontrar e divulgar cupons dessas marcas, pois elas têm maior probabilidade de atrair clientes.")
    except KeyError:
        st.error("As colunas 'brand' ou 'desconto' não foram encontradas no DataFrame após os filtros.")

    try:
        st.subheader("Distribuição de Descontos")
        fig_discount = px.histogram(df_filtered, x='desconto', nbins=20, title='Distribuição de Descontos')
        st.plotly_chart(fig_discount)
        st.info(
            "Observe a distribuição dos valores de desconto. Cupons que oferecem descontos dentro das faixas mais comuns podem ter um apelo mais amplo, enquanto descontos significativamente maiores podem criar um senso de urgência e atrair mais atenção.")
    except KeyError:
        st.error("A coluna 'desconto' não foi encontrada no DataFrame após os filtros.")

    try:
        st.subheader("Número de Produtos por Marca")
        brand_counts = df_filtered['brand'].value_counts().reset_index()
        brand_counts.columns = ['brand', 'count']
        fig_brand_count = px.bar(brand_counts.head(10), x='brand', y='count',
                                 title='Top 10 Marcas por Número de Produtos')
        st.plotly_chart(fig_brand_count)
        st.info(
            "Saiba quais marcas têm a maior variedade de produtos. Isso pode indicar um maior potencial para encontrar cupons diversos dentro dessas marcas.")
    except KeyError:
        st.error("A coluna 'brand' não foi encontrada no DataFrame após os filtros.")

st.subheader("Distribuição de Percentuais de Desconto")
try:
    fig_percentual_desconto = px.histogram(df_filtered, x='percentual_desconto', nbins=20, title='Distribuição de Percentuais de Desconto')
    st.plotly_chart(fig_percentual_desconto)
    st.info("Esta distribuição mostra a frequência dos diferentes níveis de desconto oferecidos. Um profissional de cupons afiliados pode usar isso para identificar as faixas de desconto mais comuns e potencialmente focar em cupons que oferecem descontos significativos.")
except KeyError:
    st.error("A coluna 'percentual_desconto' não foi encontrada no DataFrame após os filtros.")

st.subheader("Percentual de Desconto Médio por Marca")
try:
    avg_discount_by_brand = df_filtered.groupby('brand')['percentual_desconto'].mean().sort_values(ascending=False).reset_index()
    fig_avg_discount_brand = px.bar(avg_discount_by_brand.head(10), x='brand', y='percentual_desconto', title='Top 10 Marcas com Maior Percentual de Desconto Médio')
    st.plotly_chart(fig_avg_discount_brand)
    st.info("Este gráfico destaca as marcas que, em média, oferecem os maiores descontos. O profissional pode priorizar a busca por cupons dessas marcas para atrair mais usuários.")
except KeyError:
    st.error("A coluna 'brand' ou 'percentual_desconto' não foram encontradas no DataFrame após os filtros.")

st.subheader("Relação entre Percentual de Desconto e Avaliação")
try:
    df_filtered_rating = df_filtered[df_filtered['rating'].notna() & df_filtered['percentual_desconto'].notna()]
    fig_discount_rating = px.scatter(df_filtered_rating, x='percentual_desconto', y='rating', color='brand',
                                     hover_data=['name', 'seller', 'percentual_desconto'],
                                     title='Percentual de Desconto vs. Avaliação do Produto')
    st.plotly_chart(fig_discount_rating)
    st.info("Este gráfico explora se há alguma correlação entre o percentual de desconto e a avaliação dos produtos. Produtos com descontos maiores tendem a ter avaliações melhores ou piores? Essa informação pode influenciar a estratégia de divulgação de cupons.")
except KeyError:
    st.error("As colunas 'percentual_desconto' ou 'rating' não foram encontradas no DataFrame após os filtros.")

st.subheader("Produtos com Maiores Descontos")
try:
    top_discounted_products = df_filtered.sort_values(by='percentual_desconto', ascending=False).head(10)
    st.dataframe(top_discounted_products[['name', 'brand', 'price_old', 'price_new', 'percentual_desconto']])
    st.info("Esta tabela lista os produtos com os maiores percentuais de desconto atualmente disponíveis, com base nos filtros aplicados. É uma informação crucial para identificar ofertas atraentes para divulgar.")
except KeyError:
    st.error("As colunas necessárias para exibir os produtos com maiores descontos não foram encontradas.")

st.subheader("Análise de Frete Grátis e Desconto")
try:
    discount_frete_gratis = df_filtered.groupby('frete_gratis')['percentual_desconto'].mean().reset_index()
    discount_frete_gratis['frete_gratis'] = discount_frete_gratis['frete_gratis'].map({True: 'Sim', False: 'Não'})
    fig_discount_frete = px.bar(discount_frete_gratis, x='frete_gratis', y='percentual_desconto',
                                 title='Percentual de Desconto Médio com Frete Grátis vs. Sem Frete Grátis')
    st.plotly_chart(fig_discount_frete)
    st.info("Este gráfico compara o percentual de desconto médio para produtos com e sem frete grátis. Ofertas que combinam um bom desconto com frete grátis podem ser especialmente eficazes para atrair clientes.")
except KeyError:
    st.error("A coluna 'frete_gratis' ou 'percentual_desconto' não foram encontradas no DataFrame após os filtros.")

# Exibir o DataFrame filtrado (opcional)
if st.checkbox("Mostrar Dados Filtrados"):
    st.subheader("Dados Filtrados")
    st.dataframe(df_filtered)