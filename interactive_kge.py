from core import KGE
from core.knowledge_graph import KG

# (1) Load a pre-trained model; Yago3-10
pre_trained_kge = KGE(path_of_pretrained_model_dir='Experiments/2022-03-16 15:24:18.899385')
# (2) Look at a particular triple's score
heads, relations, tails = ['Boo_Young-tae'], ['playsFor'], ['Yangju_Citizen_FC']
s = pre_trained_kge.triple_score(head_entity=heads, relation=relations, tail_entity=tails)
# (3) Train Model on KGs/SubYAGO3-10/train.txt contains single triple (Chatou,isLocatedIn,France)
kg = KG("KGs/SubYAGO3-10", entity_to_idx=pre_trained_kge.entity_to_idx, relation_to_idx=pre_trained_kge.relation_to_idx)
pre_trained_kge.train(kg, lr=.1, epoch=50, batch_size=32, neg_sample_ratio=10, num_workers=4)
# (4) Look at the score again
m = f'Score({heads[0]},{relations[0]},{tails[0]})={s}'
print('Before:', m)
s = pre_trained_kge.triple_score(head_entity=heads,
                                 relation=relations, tail_entity=tails)
m = f'Score({heads[0]},{relations[0]},{tails[0]})={s}'
print('After:', m)
# (5) Save this model
pre_trained_kge.save()


def predictions():
    """ Prediction on UMLS dataset"""
    # (3) Triple score: <entity, relation,entity>
    triple_score = pre_trained_kge.predict_topk(head_entity=['eicosanoid'],
                                                relation=['interacts_with'],
                                                tail_entity=['eicosanoid'])
    print(triple_score)

    # (4) Randomly sampled triple score: <entity, relation,entity>
    triple_score = pre_trained_kge.predict_topk(head_entity=pre_trained_kge.sample_entity(1),
                                                relation=pre_trained_kge.sample_relation(1),
                                                tail_entity=pre_trained_kge.sample_entity(1))
    print(triple_score)

    # (5) Head entity prediction : <?,relation,entity>
    scores_and_entities = pre_trained_kge.predict_topk(relation=['interacts_with'], tail_entity=['eicosanoid'], k=10)
    print([i for i in scores_and_entities])
    # (6) Tail entity prediction : <entity,relation,?>
    scores_and_entities = pre_trained_kge.predict_topk(head_entity=['eicosanoid'],
                                                       relation=['interacts_with'], k=10)
    print([i for i in scores_and_entities])
    # (7) Relation prediction : <entity,?relation>
    scores_and_relations = pre_trained_kge.predict_topk(head_entity=['eicosanoid'],
                                                        tail_entity=['eicosanoid'], k=10)
    print([i for i in scores_and_relations])


"""
# Selective Continual Training
# Load DBpedia page of something
import requests as req
import os

triples = req.get("https://dbpedia.org/data/Albert_Einstein.ntriples").text
os.system('mkdir Dummy')
with open('Dummy/train', 'w') as w:
    w.writelines(triples)
"""
