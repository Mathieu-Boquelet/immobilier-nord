import streamlit as st
import pandas as pd
import altair as alt

st.title('Prix de l\'immobilier dans le Nord')
st.caption("Source : DVF (data.gouv.fr). Prix médian au m² par commune.")

df = pd.read_csv('dvf_59_propre.csv')

st.sidebar.header("Filtres")
st.write('Nombre de ventes :', len(df))
st.dataframe(df) #(df.head(50))

type_bien = st.selectbox("type de bien", df['type_local'].unique())
d = df[df["type_local"] == type_bien]
st.write("Ventes pour ce type :", len(d))
min_ventes = st.slider("Nombre minimum de ventes", 10, 100, 50)
ordre = st.sidebar.radio("Ordre du classement", ["Décroissant", "Croissant"])
nb_communes = st.sidebar.slider("Nombre de communes affichées", 5, 30, 10)

d = df[df['type_local'] == type_bien]

stats = d.groupby("nom_commune")['prix au m2'].agg(
    prix_moyen = 'mean',
    prix_median = 'median',
    nb_ventes = 'count'
)
stats = stats[stats['nb_ventes'] >= min_ventes]
croissant = (ordre == "Croissant")
stats = stats.sort_values('prix_median', ascending=croissant).reset_index()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Communes analysées", len(stats))
col2.metric("Prix médian Global (€/m²)", f"{d['prix au m2'].median():,.0f}".replace(",", " "))
col3.metric("Prix moyen Global (€/m²)", f"{d['prix au m2'].mean():,.0f}".replace(",", " "))
col4.metric("Ventes analysées", len(d))

top = stats.head(nb_communes)
graphique = alt.Chart(top).mark_bar().encode(
    x=alt.X("prix_median:Q", title="Prix médian (€/m²)"),
    y=alt.Y("nom_commune:N", sort=None, title=""),
    tooltip=[
        alt.Tooltip("nom_commune:N", title="Commune"),
        alt.Tooltip("prix_median:Q", title="Prix médian (€/m²)", format=",.0f"),
        alt.Tooltip("nb_ventes:Q", title="Nombre de ventes"),
    ],
)
st.subheader(f"{type_bien} : {ordre.lower()}, top {nb_communes}")
st.altair_chart(graphique, use_container_width=True)

with st.expander("Voir le tableau complet"):
    st.dataframe(stats, use_container_width=True)



st.subheader("Évolution du prix médian au m²")

d = d.copy()
d["date_mutation"] = pd.to_datetime(d["date_mutation"])
d["mois"] = d["date_mutation"].dt.to_period("M").dt.to_timestamp()

communes = st.multiselect(
    "Communes à comparer",
    sorted(d["nom_commune"].unique()),
    default=["Lille"] if "Lille" in d["nom_commune"].values else None,
)

if communes:
    evol = (
        d[d["nom_commune"].isin(communes)]
        .groupby(["mois", "nom_commune"])["prix au m2"]
        .median()
        .reset_index()
    )
    courbe = alt.Chart(evol).mark_line(point=True).encode(
        x=alt.X("mois:T", title="Mois"),
        y=alt.Y("prix au m2:Q", title="Prix médian (€/m²)"),
        color=alt.Color("nom_commune:N", title="Commune"),
        tooltip=[
            alt.Tooltip("nom_commune:N", title="Commune"),
            alt.Tooltip("mois:T", title="Mois", format="%m/%Y"),
            alt.Tooltip("prix au m2:Q", title="Prix médian", format=",.0f"),
        ],
    )
    st.altair_chart(courbe, use_container_width=True)
else:
    st.info("Choisis au moins une commune.")