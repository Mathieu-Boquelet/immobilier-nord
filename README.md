# Immobilier Nord : dashboard des prix au m²

Dashboard interactif qui analyse les prix de l'immobilier dans le département du Nord (59) à partir des données DVF.

🔗 **Démo en ligne : https://immobilier-nord.streamlit.app/ **

## Fonctionnalités
- Classement des communes par prix médian au m² (croissant ou décroissant)
- Filtres : type de bien (appartement ou maison), nombre minimum de ventes, nombre de communes affichées
- Chiffres clés : nombre de communes, prix médian global, nombre de ventes
- Évolution du prix médian dans le temps, avec comparaison de plusieurs communes

## Données
Source : [Demandes de valeurs foncières (DVF)](https://www.data.gouv.fr), data.gouv.fr.
Le notebook `nettoyage_dvf.ipynb` documente le nettoyage :
- sélection des ventes d'appartements et de maisons
- suppression des ventes multi-lots (prix répété sur plusieurs lignes)
- calcul du prix au m² et filtrage des valeurs aberrantes (surface < 15 m², prix hors de 800-8000 €/m²)

## Technologies
Python, pandas, Altair, Streamlit

## Lancer le projet en local
pip install -r requirements.txt
streamlit run app.py

## Limites
- Les prix sont des médianes sur les ventes retenues après nettoyage ; les communes avec peu de ventes sont exclues.
- Le prix au m² des maisons est calculé sur la surface bâtie, sans le terrain.
