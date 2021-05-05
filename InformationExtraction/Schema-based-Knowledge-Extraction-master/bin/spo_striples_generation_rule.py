#coding=gbk
from itertools import permutations
import operator
import random
from .spo_striples_generation_data_manage import Sorted_relation_and_entity_list_Management
from .priori_statistical_information import Priori_statistical_information
#from .priori_statistical_information_from_file import Priori_statistical_information
from .spo_pattern_matching_extraction_rule import SPO_pattern_matching

# ͨ��ģ�ͽ������ʽ���� spo_list
class SPO_List_Heuristic_Generation(Priori_statistical_information):

    def __init__(self):
        Priori_statistical_information.__init__(self)
        self.spo_predicate_temple = SPO_Predicate_Temple()
        self.relational_location_word = {
            '�漮': ["�漮"], '������': ["����", "������", "��"],
            '����': ['����', "�ݳ�", "����"], '����': ['����',"���"], '����': ['����'],
            "����": ["����", "ִ��"], '��Ƭ��': ["��Ƭ"], '���': ['���'], '����': ['����', "����"],
            '����': ['����'], 'ĸ��': ['ĸ��'], '����': ['����', "��", "Ů��"], '�ɷ�': ['�ɷ�', "��"],
            '���³�': ['���³�', '����'], '��ʼ��': ["��ʼ��", "��ʼ", "����", "����"],
            '������': ['������', '����', "����"], '�α�': ['�α�',"��ί"],
        }

    def create_new_spo_item(self, a_relationship=None, subject_type=None, object_type=None, subject_value=None,
                            object_value=None):
        spo_item = dict()
        spo_item["predicate"] = a_relationship
        spo_item["object_type"] = object_type
        spo_item["subject_type"] = subject_type
        spo_item["object"] = object_value
        spo_item["subject"] = subject_value
        return spo_item

    def get_entity_value_list_by_name(self, entity_name, sort_entity_list):
        return [entity_value for entity_type, entity_value in sort_entity_list if entity_type == entity_name]

    def heuristic_generate_zuji_chushengdi(self, text_sentence, need_analysis_relation_flag_dict,
                                                        sort_entity_list):
        spo_list = []
        didian_list = self.get_entity_value_list_by_name("�ص�", sort_entity_list)
        renwu_list = self.get_entity_value_list_by_name("����", sort_entity_list)
        didian_list_len = len(didian_list)
        for renwu in renwu_list:
            if didian_list_len == 1:
                if need_analysis_relation_flag_dict["�漮"] == 1:
                    spo_item = self.create_new_spo_item("�漮", '�ص�', '����', didian_list[0], renwu)
                    spo_list.append(spo_item)
            if didian_list_len >= 2:
                relational_location_word_list = self.relational_location_word["�漮"]
                for relational_location_word in relational_location_word_list:
                    if relational_location_word in text_sentence:
                        nearest_didian_word = self.find_word_B_nearest_to_word_A_for_single_relation(
                            text_sentence, relational_location_word, didian_list)
                        if nearest_didian_word is not None and nearest_didian_word in didian_list:
                            spo_item = self.create_new_spo_item("�漮", "�ص�", "����", nearest_didian_word, renwu)
                            spo_list.append(spo_item)
                            didian_list.remove(nearest_didian_word)
                        break
                for didian in didian_list:
                    spo_item = self.create_new_spo_item("������", "�ص�", "����", didian, renwu)
                    spo_list.append(spo_item)
        if len(spo_list) == 0:
            for relation_name, relation_flag in need_analysis_relation_flag_dict.items():
                if relation_flag == 1:
                    spo_list.extend(self.spo_predicate_temple.temple_priori_information(relation_name, text_sentence))
        return spo_list

    # ����['����', '����', '����']��ϵͨ���ʵľ����ϵ
    def handle_geshou_zuoci_zuoqu_by_word_distence(self, text_sentence, need_analysis_relation_flag_dict, renwu_list, gequ_list):
        spo_list = []
        for gequ in gequ_list:
            nearest_renwu_word_list = [None, None, None]
            for idx, relation_name in enumerate(['����', '����', '����']):
                if need_analysis_relation_flag_dict[relation_name] == 1:
                    relational_location_word_list = self.relational_location_word[relation_name]
                    for relational_location_word in relational_location_word_list:
                        if relational_location_word in text_sentence:
                            nearest_renwu_word = self.find_word_B_nearest_to_word_A_for_single_relation(
                                text_sentence, relational_location_word, renwu_list)
                            nearest_renwu_word_list[idx] = nearest_renwu_word
                            break
            for relation_name, nearest_renwu_word in zip(['����', '����', '����'], nearest_renwu_word_list):
                if nearest_renwu_word is not None and nearest_renwu_word in renwu_list:
                    spo_item = self.create_new_spo_item(relation_name, "����", "����", nearest_renwu_word, gequ)
                    spo_list.append(spo_item)
                    renwu_list.remove(nearest_renwu_word)
            if len(renwu_list) > 0:
                for renwu in renwu_list:
                    spo_item = self.create_new_spo_item('����', "����", "����", renwu, gequ)
                    spo_list.append(spo_item)
        return spo_list

    #��������Ƭ�˱����Ա��ϵͨ���ʵľ����ϵ
    def handle_daoyan_zhipianren_bianju_zhuyan_by_word_distence(self, text_sentence, need_analysis_relation_flag_dict, renwu_list, yingshizuopin):
        spo_list = []
        nearest_renwu_word_list = [None, None, None]
        for idx, relation_name in enumerate(["����","��Ƭ��","���"]):
            if need_analysis_relation_flag_dict[relation_name] == 1:
                relational_location_word_list = self.relational_location_word[relation_name]
                for relational_location_word in relational_location_word_list:
                    if relational_location_word in text_sentence:
                        nearest_renwu_word = self.find_word_B_nearest_to_word_A_for_single_relation(
                            text_sentence, relational_location_word, renwu_list)
                        nearest_renwu_word_list[idx] = nearest_renwu_word
                        break
        for relation_name, nearest_renwu_word in  zip(["����","��Ƭ��","���"], nearest_renwu_word_list):
            if nearest_renwu_word is not None and nearest_renwu_word in renwu_list:
                spo_item = self.create_new_spo_item(relation_name, "����", "Ӱ����Ʒ", nearest_renwu_word, yingshizuopin)
                spo_list.append(spo_item)
                renwu_list.remove(nearest_renwu_word)
        if len(renwu_list) > 0:
            for renwu in renwu_list:
                spo_item = self.create_new_spo_item("����", "����", "Ӱ����Ʒ", renwu, yingshizuopin)
                spo_list.append(spo_item)
        return spo_list

    # �ں�ѡ���б� candidate_word_list ���ҳ��������Ĵ� center_word ����Ĵ���
    def find_word_B_nearest_to_word_A_for_single_relation(self, text_sentence, center_word, candidate_word_list):
        candidate_word_list_distance = []
        if center_word in text_sentence:
            word_A_index = text_sentence.index(center_word) + len(center_word) / 2
            candidate_word_list.reverse()  # �б�˳����Ϊ�˵����������ʾ������Ĵ���ͬ����ʱ�����ȷ����ұߵĵ���
        else:
            word_A_index = 0
        for candidate_word in candidate_word_list:
            if candidate_word in text_sentence:
                candidate_word_index = text_sentence.index(candidate_word) + len(candidate_word) / 2
            else:
                candidate_word_index = 1000
            candidate_word_list_distance.append(abs(candidate_word_index - word_A_index))
        if len(candidate_word_list_distance) > 0:
            nearest_word = candidate_word_list[candidate_word_list_distance.index(min(candidate_word_list_distance))]
            return nearest_word
        else:
            return ""

    def heuristic_handle_multiple_relations(self, text_sentence, need_analysis_relation_flag_dict, sort_entity_list):
        spo_list = []
        if "����" in need_analysis_relation_flag_dict: # ����('����', '����'): ['����', '����', 'ĸ��', '�ɷ�'],
            spo_list.extend(self.heuristic_generate_fuqin_muqin_zhangfu_qizi(
                text_sentence, need_analysis_relation_flag_dict, sort_entity_list))
        elif "����" in need_analysis_relation_flag_dict:#���� ('����', 'Ӱ����Ʒ'): ['����', '��Ƭ��', '���', '����']
            spo_list.extend(self.heuristic_generate_daoyan_zhipian_bianju_zhuyan(
                text_sentence, need_analysis_relation_flag_dict, sort_entity_list))
        elif "��" in need_analysis_relation_flag_dict:#���� ('Text', '��ʷ����'): ['��', '����', '��'],
            spo_list.extend(self.heuristic_generate_zi_chaodai_hao(
                text_sentence, need_analysis_relation_flag_dict, sort_entity_list))
        elif "����" in need_analysis_relation_flag_dict:#���� ('����', '����'): ['����', '����', '����'],
            spo_list.extend(self.heuristic_generate_geshou_zuoci_zuoqu(
                text_sentence, need_analysis_relation_flag_dict, sort_entity_list))
        elif "�漮" in need_analysis_relation_flag_dict:
            spo_list.extend(self.heuristic_generate_zuji_chushengdi(
                text_sentence, need_analysis_relation_flag_dict, sort_entity_list))
        elif "���³�" in need_analysis_relation_flag_dict:
            spo_list.extend(self.heuristic_generate_dongshizhang_chuangshiren(
                text_sentence, need_analysis_relation_flag_dict, sort_entity_list))
        elif "������" in need_analysis_relation_flag_dict:
            spo_list.extend(self.heuristic_generate_zhuchiren_jiabin(
                text_sentence, need_analysis_relation_flag_dict, sort_entity_list))
        else:
            pass
        return spo_list

    # ('����', '��������'): ['������', '�α�']
    def heuristic_generate_zhuchiren_jiabin(self, text_sentence, need_analysis_relation_flag_dict,
                                                        sort_entity_list):
        spo_list = []
        renwu_list = self.get_entity_value_list_by_name("����", sort_entity_list)
        dianshizongyi_list = self.get_entity_value_list_by_name("��������", sort_entity_list)
        renwu_list_len = len(renwu_list)
        dianshizongyi_list_len = len(dianshizongyi_list)
        if dianshizongyi_list_len > 0:
            for dianshizongyi in dianshizongyi_list:
                if renwu_list_len == 1:
                    for zhuchi_feature_word in ['������', '����', "����"]:
                        if zhuchi_feature_word in text_sentence:
                            spo_item = self.create_new_spo_item("������", "����", "��������", renwu_list[0], dianshizongyi)
                            spo_list.append(spo_item)
                            break
                    if "�α�" in text_sentence:
                        spo_item = self.create_new_spo_item("�α�", "����", "��������", renwu_list[0], dianshizongyi)
                        spo_list.append(spo_item)
                elif renwu_list_len >= 2:
                    if "������" in text_sentence and "�α�" in text_sentence:
                        for relation_name, relation_flag in need_analysis_relation_flag_dict.items():
                            spo_list.extend(
                                self.spo_predicate_temple.temple_priori_information(relation_name, text_sentence))
                    else:
                        for zhuchi_feature_word in ['������', '����', "����"]:
                            if zhuchi_feature_word in text_sentence:
                                for renwu in renwu_list:
                                    spo_item = self.create_new_spo_item("������", "����", "��������", renwu, dianshizongyi)
                                    spo_list.append(spo_item)
                                break
                            else:
                                for renwu in renwu_list:
                                    spo_item = self.create_new_spo_item("�α�", "����", "��������", renwu, dianshizongyi)
                                    spo_list.append(spo_item)
                                break
        #ʹ������֪ʶ��׽
        if len(spo_list) == 0:
            for relation_name, relation_flag in need_analysis_relation_flag_dict.items():
                    spo_list.extend(self.spo_predicate_temple.temple_priori_information(relation_name, text_sentence))
        return spo_list

    def heuristic_generate_geshou_zuoci_zuoqu(self, text_sentence, need_analysis_relation_flag_dict,
                                                        sort_entity_list):
        spo_list = []
        #ʹ������֪ʶ��׽
        for relation_name, relation_flag in need_analysis_relation_flag_dict.items():
            if relation_flag == 1:
                spo_list.extend(self.spo_predicate_temple.temple_priori_information(relation_name, text_sentence))
        if len(spo_list) == 0:
            gequ_list = self.get_entity_value_list_by_name("����", sort_entity_list)
            renwu_list = self.get_entity_value_list_by_name("����", sort_entity_list)
            renwu_list_len = len(renwu_list)
            for gequ in gequ_list:
                if renwu_list_len == 1:
                    for relation_name, relation_flag in need_analysis_relation_flag_dict.items():
                        if relation_flag == 1:
                            spo_item = self.create_new_spo_item(relation_name, "����", "����", renwu_list[0], gequ)
                            spo_list.append(spo_item)
                elif renwu_list_len == 2:
                      renwu_2_index = 0
                      for relation_name, relation_flag in need_analysis_relation_flag_dict.items():
                          if relation_flag == 1 and renwu_2_index == 0:
                              renwu_2_index += 1
                              spo_item = self.create_new_spo_item(relation_name, "����", "����", renwu_list[0], gequ)
                          else:
                              spo_item = self.create_new_spo_item(relation_name, "����", "����", renwu_list[1], gequ)
                          spo_list.append(spo_item)
                elif renwu_list_len >= 3:
                    spo_list.extend(self.handle_geshou_zuoci_zuoqu_by_word_distence(
                        text_sentence, need_analysis_relation_flag_dict, renwu_list, gequ_list))

        return spo_list

    def heuristic_generate_dongshizhang_chuangshiren(self, text_sentence, need_analysis_relation_flag_dict,
                                                        sort_entity_list):
        spo_list = []
        for relation_name in ['���³�', '��ʼ��']:
            spo_list.extend(self.spo_predicate_temple.temple_priori_information(
                relation_name=relation_name, text_sentence=text_sentence))
        return spo_list

    def heuristic_generate_zi_chaodai_hao(self, text_sentence, need_analysis_relation_flag_dict,
                                                        sort_entity_list):
        spo_list = []
        for relation_name in ['��', '����', '��']:
            spo_list.extend(self.spo_predicate_temple.temple_priori_information(
                relation_name=relation_name, text_sentence=text_sentence))
        return spo_list

    # ('����', 'Ӱ����Ʒ'): ['����', '��Ƭ��', '���', '����']
    def heuristic_generate_daoyan_zhipian_bianju_zhuyan(self,text_sentence, need_analysis_relation_flag_dict, sort_entity_list):
        def yingshizuopin_two_ren_distence():
            pass
        spo_list = []
        #print("heuristic_generate_daoyan_zhipian_bianju_zhuyan:\t",need_analysis_relation_flag_dict)
        yingshizuopin_list = self.get_entity_value_list_by_name("Ӱ����Ʒ", sort_entity_list)
        renwu_list = self.get_entity_value_list_by_name("����", sort_entity_list)
        yingshizuopin_list_len = len(yingshizuopin_list)
        renwu_list_len = len(renwu_list)
        #��ֻ��һ��Ӱ����Ʒ��ǰ���½�������ʽ�Ƶ�������ֱ��ʹ������֪ʶ
        if yingshizuopin_list_len == 1:
            if renwu_list_len == 1:
                for relation_name, relation_flag in need_analysis_relation_flag_dict.items():
                    if relation_flag == 1:
                        spo_item = self.create_new_spo_item(relation_name, "����", "Ӱ����Ʒ", renwu_list[0],
                                                            yingshizuopin_list[0])
                        spo_list.append(spo_item)
            elif renwu_list_len == 2:
                  renwu_2_index = 0
                  for relation_name, relation_flag in need_analysis_relation_flag_dict.items():
                      if relation_flag == 1 and renwu_2_index == 0:
                          renwu_2_index += 1
                          spo_item = self.create_new_spo_item(relation_name, "����", "Ӱ����Ʒ", renwu_list[0],
                                                              yingshizuopin_list[0])
                      else:
                          spo_item = self.create_new_spo_item(relation_name, "����", "Ӱ����Ʒ", renwu_list[1],
                                                              yingshizuopin_list[0])
                      spo_list.append(spo_item)
            elif renwu_list_len >= 3:
                spo_list.extend(self.handle_daoyan_zhipianren_bianju_zhuyan_by_word_distence(
                    text_sentence, need_analysis_relation_flag_dict, renwu_list, yingshizuopin_list[0]))
        else:
            for relation_name, relation_flag in need_analysis_relation_flag_dict.items():
                if relation_flag == 1:
                    spo_list.extend(self.spo_predicate_temple.temple_priori_information(relation_name, text_sentence))
        return spo_list


class SPO_Predicate_Temple(SPO_pattern_matching, Priori_statistical_information):

    def __init__(self):
        SPO_pattern_matching.__init__(self)
        Priori_statistical_information.__init__(self)

    def create_new_spo_item(self, a_relationship=None, subject_type=None, object_type=None, subject_value=None,
                            object_value=None):
        spo_item = dict()
        spo_item["predicate"] = a_relationship
        spo_item["object_type"] = object_type
        spo_item["subject_type"] = subject_type
        spo_item["object"] = object_value
        spo_item["subject"] = subject_value
        return spo_item

    def get_entity_value_list_by_name(self, entity_name, sort_entity_list):
        return [entity_value for entity_type, entity_value in sort_entity_list if entity_type == entity_name]

    # ͨ��ģ�壬������п��ܵ�spoƥ���ϵ���� spo_list
    def temple_one(self, relation_name, sort_entity_list):  #
        spo_list = list()
        subject_type = self.schemas_dict_relation_2_subject_object[relation_name][0][0]
        object_type = self.schemas_dict_relation_2_subject_object[relation_name][0][1]
        subject_value_list = self.get_entity_value_list_by_name(subject_type, sort_entity_list)
        object_value_list = self.get_entity_value_list_by_name(object_type, sort_entity_list)
        for subject_value in subject_value_list:
            for object_value in object_value_list:
                spo_item = self.create_new_spo_item(relation_name, subject_type, object_type, subject_value, object_value)
                spo_list.append(spo_item)
        return spo_list

    def temple_priori_information(self, relation_name, text_sentence):
        spo_list = list()
        candidate_combination_set = set()
        entityA_2_entityB_set_dict = dict()
        subject_type = self.schemas_dict_relation_2_subject_object[relation_name][0][0]
        object_type = self.schemas_dict_relation_2_subject_object[relation_name][0][1]

        # ('�ص�', '����'): ['�漮', '������'],
        if relation_name == "�漮":
            entityA_2_entityB_set_dict = self.special_entity_map_zu_ji_2_ren_wu
        elif relation_name == "������":
            entityA_2_entityB_set_dict = self.special_entity_map_chu_sheng_di_2_ren_wu
        # ('����', '��ҵ'): ['���³�', '��ʼ��']
        elif relation_name == "���³�":
            entityA_2_entityB_set_dict = self.special_entity_map_dong_shi_zhang_2_qiye
        elif relation_name == "��ʼ��":
            entityA_2_entityB_set_dict = self.special_entity_map_chuang_shi_ren_2_qiye
        # ('����', '��������'): ['������', '�α�']
        elif relation_name == "������":
            entityA_2_entityB_set_dict = self.special_entity_map_zhu_chi_ren_2_dian_shi_zong_yi
        elif relation_name == "�α�":
            entityA_2_entityB_set_dict = self.special_entity_map_jia_bin_2_dian_shi_zong_yi
        # ('Number', '������'): ['���', '�˿�����']
        elif relation_name == "���" :
            entityA_2_entityB_set_dict = self.special_entity_map_mian_ji_2_xing_zheng_qu
        elif relation_name == "�˿�����" :
            entityA_2_entityB_set_dict = self.special_entity_map_ren_kou_shu_liang_2_xing_zheng_qu
        # ('Text', '��ʷ����'): ['��', '����', '��']
        elif relation_name == "��":
            entityA_2_entityB_set_dict = self.special_entity_map_zi_2_li_shi_ren_wu
        elif relation_name == "����":
            entityA_2_entityB_set_dict = self.special_entity_map_chao_dai_2_li_shi_ren_wu
        elif relation_name == "��":
            entityA_2_entityB_set_dict = self.special_entity_map_hao_2_li_shi_ren_wu
        # ('����', '����'): ['����', '����', '����']
        elif relation_name == "����":
            entityA_2_entityB_set_dict = self.special_entity_map_ge_shou_2_ge_qu
        elif relation_name == "����":
            entityA_2_entityB_set_dict = self.special_entity_map_zuo_ci_2_ge_qu
        elif relation_name == "����":
            entityA_2_entityB_set_dict = self.special_entity_map_zuo_qu_2_ge_qu
        # ('����', '����'): ['����', '����', 'ĸ��', '�ɷ�']
        elif relation_name == "����":
            entityA_2_entityB_set_dict = self.special_entity_map_fu_qin_2_zi_nv
        elif relation_name == "ĸ��":
            entityA_2_entityB_set_dict = self.special_entity_map_mu_qin_2_zi_nv
        elif relation_name == "�ɷ�":
            entityA_2_entityB_set_dict = self.special_entity_map_zhang_fu_2_pei_ou
        elif relation_name == "����":
            entityA_2_entityB_set_dict = self.special_entity_map_qi_zi_2_pei_ou
        # ('����', 'Ӱ����Ʒ'): ['����', '��Ƭ��', '���', '����']
        elif relation_name == "����":
            entityA_2_entityB_set_dict = self.special_entity_map_dao_yan_2_ying_shi_zuo_pin
        elif relation_name == "��Ƭ��":
            entityA_2_entityB_set_dict = self.special_entity_map_zhi_pian_ren_2_ying_shi_zuo_pin
        elif relation_name == "���":
            entityA_2_entityB_set_dict = self.special_entity_map_bian_ju_2_ying_shi_zuo_pin
        elif relation_name == "����":
            entityA_2_entityB_set_dict = self.special_entity_map_zhu_yan_2_ying_shi_zuo_pin
        elif relation_name == "��������":
            entityA_2_entityB_set_dict = self.special_entity_map_special_entity_shi_jien_2_qi_ye


        if relation_name in ["�漮", "������", "���³�", "��ʼ��", "������", "�α�", '���', '�˿�����',
                            '��', '����', '��', '����', '����', 'ĸ��', '�ɷ�', '����', '��Ƭ��', '���', '����',
                             "��������" ]:
            for spo_subject, spo_object_set in entityA_2_entityB_set_dict.items():
                for spo_object in spo_object_set:
                    if spo_subject in text_sentence and spo_object in text_sentence:
                        candidate_combination_set.add((spo_subject, spo_object))

        if relation_name in ['����', '����', '����']: # ('����', '����'): ['����', '����', '����']
            for spo_subject, spo_object_set in entityA_2_entityB_set_dict.items():
                for spo_object in spo_object_set:
                    if spo_subject in text_sentence and "��{}��".format(spo_object) in text_sentence:
                        candidate_combination_set.add((spo_subject, spo_object))

        for spo_subject, spo_object in candidate_combination_set:
            spo_item = self.create_new_spo_item(relation_name, subject_type, object_type, spo_subject, spo_object)
            spo_list.append(spo_item)
        return spo_list

class SPO_Generation_Rule_Base(SPO_pattern_matching, Priori_statistical_information):

    def __init__(self):
        SPO_pattern_matching.__init__(self)
        Priori_statistical_information.__init__(self)

    # �� 0.5 Ϊ��׼����Ԥ��Ŀ��ܵĹ�ϵ
    def _split_relationship_by_score(self, sort_list):
        sort_list_positive = []
        sort_list_negative = []
        for relationship, value in sort_list:
            if value > 0.5:
                sort_list_positive.append(relationship)
            else:
                sort_list_negative.append(relationship)
        return sort_list_positive, sort_list_negative

    # �Թ�ϵ��Ӧ�������ֹ�ϵ
    def _split_relationship_by_single_or_multiple(self, relation_list):
        #single: ('��ҵ', 'Ӱ����Ʒ')->['��Ʒ��˾'], multiple: ('����', '����')->['����', '����', '����']
        single_list, multiple_list = [], []
        single_relation_list = ["�ܲ��ص�", "Ŀ", "���", "��ӳʱ��", "����ר��", "ע���ʱ�", "�׶�", "���",
                                "��Ʒ��˾", "��ҵ����", "��������", "����", "����", "������վ", "����", "������",
                                "רҵ����", "����", "��ҵԺУ", "ռ�����", "�ٷ�����", "��������",
                                "���ڳ���", "����", "����", "�ı���", '��������']
        multiple_relation_list = ["�漮", "������", "���³�", "��ʼ��", "������", "�α�", '���', '�˿�����',
                                  '��', '����', '��', '����', '����', '����', '����', '����', 'ĸ��', '�ɷ�',
                                 '����', '��Ƭ��', '���', '����']
        for relation in relation_list:
            if relation in single_relation_list:
                single_list.append(relation)
            if relation in multiple_relation_list:
                multiple_list.append(relation)
        return single_list, multiple_list


    def rule_generate_spo_list(self, text_sentence, sort_relation_list, sort_entity_list, refer_spo_list):
        raise NotImplemented("need a function that return spo_list")

    # ͨ�������ʣ�ȡ�ᡰ�漮���������ء���ϵ
    def distinguishing_zu_ji_and_chu_sheng_di_relation(self, combine_relation_list, text_sentence):
        zu_ji_flag, zuji_value = self.spo_pattern_matching_extraction_rule_by_relation("�漮", text_sentence)
        if "�漮" in combine_relation_list and "������" in combine_relation_list:
            if zu_ji_flag == False or zuji_value is None:
                combine_relation_list.remove("�漮")
        return combine_relation_list

    # ͨ�������ʣ�ȡ�ᡰ���³�������ʼ�ˡ���ϵ
    def distinguishing_chuang_shi_ren_and_dong_shi_zhang(self, combine_relation_list, text_sentence):
        dong_shi_zhang_flag, dong_shi_zhang_value = self.spo_pattern_matching_extraction_rule_by_relation("���³�", text_sentence)
        chuang_shi_ren_flag, chuang_shi_ren_value = self.spo_pattern_matching_extraction_rule_by_relation("��ʼ��", text_sentence)
        if "���³�" not in combine_relation_list and dong_shi_zhang_flag == True:
            combine_relation_list.append("���³�")
        if "��ʼ��" not in combine_relation_list and chuang_shi_ren_flag == True:
            combine_relation_list.append("��ʼ��")
        return combine_relation_list

    # ͨ�������ʣ�ȡ�ᡰ�α����������ˡ���ϵ
    def distinguishing_zhu_chi_ren_and_jia_bin(self, combine_relation_list, text_sentence):

        zhu_chi_ren_flag, zhu_chi_ren_value = self.spo_pattern_matching_extraction_rule_by_relation("������", text_sentence)
        jia_bin_flag, jia_bin_value = self.spo_pattern_matching_extraction_rule_by_relation("�α�", text_sentence)
        if "������" not in combine_relation_list and zhu_chi_ren_flag == True:
            combine_relation_list.append("������")
        if "�α�" not in combine_relation_list and jia_bin_flag == True:
            combine_relation_list.append("�α�")
        return combine_relation_list

    # ͨ�������ʣ�ȡ�ᡰ��������˿���������ϵ
    def distinguishing_mian_ji_and_ren_kou_shu_liang(self, combine_relation_list, text_sentence):
        mian_ji_flag, mian_ji_value = self.spo_pattern_matching_extraction_rule_by_relation("���", text_sentence)
        ren_kou_shu_liang_flag, ren_kou_value = self.spo_pattern_matching_extraction_rule_by_relation("�˿�����", text_sentence)
        if "���" not in combine_relation_list and mian_ji_flag == True:
            combine_relation_list.append("���")
        if "�˿�" not in combine_relation_list and ren_kou_shu_liang_flag == True:
            combine_relation_list.append("�˿�����")
        return combine_relation_list

    # ͨ�������ʣ�ȡ�ᡰ�֡������������š���ϵ
    def distinguishing_zi_chao_dai_and_hao(self, combine_relation_list, text_sentence):
        zi_flag, zi_value = self.spo_pattern_matching_extraction_rule_by_relation("��", text_sentence)
        chao_dai_flag, chao_dai_value = self.spo_pattern_matching_extraction_rule_by_relation("����", text_sentence)
        hao_flag, hao_value = self.spo_pattern_matching_extraction_rule_by_relation("��", text_sentence)
        if "��" not in combine_relation_list and zi_flag == True:
            combine_relation_list.append("��")
        if "����" not in combine_relation_list and chao_dai_flag == True:
            combine_relation_list.append("����")
        if "��" not in combine_relation_list and hao_flag == True:
            combine_relation_list.append("��")
        return combine_relation_list

    # ͨ�������ʣ�ȡ�ᡰ���֡������ʡ�����������ϵ
    def distinguishing_ge_shou_zuo_ci_and_zuo_qu(self, combine_relation_list, text_sentence):
        ge_shou_flag, ge_shou_value = self.spo_pattern_matching_extraction_rule_by_relation("����", text_sentence)
        zuo_ci_flag, zuo_ci_value = self.spo_pattern_matching_extraction_rule_by_relation("����", text_sentence)
        zuo_qu_flag, zuo_qu_value = self.spo_pattern_matching_extraction_rule_by_relation("����", text_sentence)
        if "����" not in combine_relation_list and ge_shou_flag == True:
            combine_relation_list.append("����")
        if "����" not in combine_relation_list and zuo_ci_flag == True:
            combine_relation_list.append("����")
        if "����" not in combine_relation_list and zuo_qu_flag == True:
            combine_relation_list.append("����")
        return combine_relation_list

    # ͨ�������ʣ�ȡ�ᡰ���ס���ĸ�ס����ɷ򡱡����ӡ���ϵ
    def distinguishing_fu_qin_mu_qin_zhang_fu_and_qi_zi(self, combine_relation_list, text_sentence):
        fu_qin_flag, fu_qin_value = self.spo_pattern_matching_extraction_rule_by_relation("����", text_sentence)
        mu_qin_flag, mu_qin_value = self.spo_pattern_matching_extraction_rule_by_relation("ĸ��", text_sentence)
        zhang_fu_flag, zhang_fu_value = self.spo_pattern_matching_extraction_rule_by_relation("�ɷ�", text_sentence)
        qi_zi_flag, qi_zi_value = self.spo_pattern_matching_extraction_rule_by_relation("����", text_sentence)
        if "����" not in combine_relation_list and fu_qin_flag == True:
            combine_relation_list.append("����")
        if "ĸ��" not in combine_relation_list and mu_qin_flag == True:
            combine_relation_list.append("ĸ��")
        if "�ɷ�" not in combine_relation_list and zhang_fu_flag == True:
            combine_relation_list.append("�ɷ�")
        if "����" not in combine_relation_list and qi_zi_flag == True:
            combine_relation_list.append("����")
        return combine_relation_list

    # ͨ�������ʣ�ȡ�ᡰ���ݡ�����Ƭ�ˡ�����硱�����ݡ���ϵ
    def distinguishing_dao_yan_zhi_pian_ren_bian_ju_and_zhu_yan(self, combine_relation_list, text_sentence):
        dao_yan_flag, dao_yan_value = self.spo_pattern_matching_extraction_rule_by_relation("����", text_sentence)
        zhi_pian_ren_flag, zhi_pian_ren_value = self.spo_pattern_matching_extraction_rule_by_relation("��Ƭ��", text_sentence)
        bian_ju_flag, bian_ju_value = self.spo_pattern_matching_extraction_rule_by_relation("���", text_sentence)
        zhu_yan_flag, zhu_yan_value = self.spo_pattern_matching_extraction_rule_by_relation("����", text_sentence)
        if "����" not in combine_relation_list and dao_yan_flag == True:
            combine_relation_list.append("����")
        if "��Ƭ��" not in combine_relation_list and zhi_pian_ren_flag == True:
            combine_relation_list.append("��Ƭ��")
        if "���" not in combine_relation_list and bian_ju_flag == True:
            combine_relation_list.append("���")
        if "����" not in combine_relation_list and zhu_yan_flag == True:
            combine_relation_list.append("����")
        return combine_relation_list


# ֱ����ģ���Ʋ�Ĺ�ϵ���Ҷ�Ӧ��Ҫ��ʵ�壬���������й�ϵ�����п���ʵ�壬������� spo_list���ٶȿ죬����׼ȷ�ʵͣ�
class Relationship_Priority_Rule(SPO_Generation_Rule_Base):
    """
    length_equal:	 0.523
    length_shorter:	 0.312
    length_longer:	 0.166
    """
    def __init__(self):
        SPO_Generation_Rule_Base.__init__(self,)

    def rule_generate_spo_list(self, text_sentence, sort_relation_list, sort_entity_list, refer_spo_list):
        """
        ����1����ϵ -> (���壬����)
            �����������Data-��������-��ҵ�� ��Data-��������-������
            ����취��1. ����Ϊ����

        ����2����ϵ���ʴ��� 0.5 �Ĵ���� sort_list_positive������� sort_list_negative
            Ĭ��ֻ�� sort_list_positive �й�ϵ���д���
            ���������sort_list_positive Ϊ�գ��򽫡�һ������Ը������ķ�����б�

        ����3��������ʵ���б��з���������߿���֮һ���ŷ����ѡ��Ԫ���б�spo_list��
            ����취������ȱ��������߿���֮һ����Ԫ��, ��������֮һ������һ����Ŀǰ�� None ��ʾ

        ����4�����ͬһ�����͵�ʵ���ж�����������ÿһ��ʵ�壬�����Ե�һ��ʵ��Ϊ���壬����ʵ��Ϊ����
        ����5��������ֹ�ϵ�����ӻ����ɷ򣬿�������һ����֪��һ��
        """
        sort_list_positive, sort_list_negative = self._split_relationship_by_score(sort_relation_list)

        # ����2
        if len(sort_list_positive) == 0:
            sort_list_positive.append(sort_list_negative[0])
        sort_entity_list = [[name, value, 0] for name, value in sort_entity_list]
        spo_list = []

        for a_relationship in sort_list_positive:
            # ����1
            subject_object_type = self.schemas_dict_relation_2_subject_object[a_relationship]
            subject_type = subject_object_type[0][0]
            object_type = subject_object_type[0][1]
            #print("{} ---> ({}, {})".format(a_relationship, subject_type, object_type))
            spo_item = dict()
            spo_item["predicate"] = a_relationship
            spo_item["object_type"] = object_type
            spo_item["subject_type"] = subject_type
            spo_item["object"] = None
            spo_item["subject"] = None

            if object_type != subject_type:
                for idx, entity_tuple in enumerate(sort_entity_list):
                    if entity_tuple[0] == subject_type:
                        spo_item["subject"] = entity_tuple[1]
                        sort_entity_list[idx][2] += 1
                    if entity_tuple[0] == object_type:
                        spo_item["object"] = entity_tuple[1]
                        sort_entity_list[idx][2] += 1
            else:
                same_type_entity_list = [entity for entity_type, entity, loc in sort_entity_list if entity_type == object_type]
                for idx, entity in enumerate(same_type_entity_list):
                    if idx == 0:
                        spo_item["subject"] = entity
                    else:
                        spo_item["object"] = entity

                    if spo_item["subject"] is not None or spo_item["object"] is not None:
                        spo_list.append(spo_item)

            # ����3
            if spo_item["subject"] is not None or spo_item["object"] is not None:
                spo_list.append(spo_item)

        spo_list.sort(key= lambda item:item['predicate'])
        # print(len(spo_list), spo_list)

        spo_list_len = len(spo_list)
        refer_spo_list_len = len(refer_spo_list)

        # if refer_spo_list_len==spo_list_len:
        def check_SPO_list():
            print("������Ϣ:")
            print(sort_relation_list)
            print(sort_entity_list)
            print(refer_spo_list)
            print("������Ϣ:")
            print("Ԥ��Ĺ�ϵ��", len(sort_list_positive), sort_list_positive)
            print("Ԥ���˳��ʵ�壺", len(sort_entity_list), sort_entity_list)
            print("���յ�SPO�б�", refer_spo_list_len, refer_spo_list)
            print("Ԥ���SPO�б�", spo_list_len, spo_list)
            print("\n")

        return spo_list


# ���ģ�����������֪ʶ��ѵ�������г�ȡ��û�������ⲿ��Դ������ spo_list��ͨ���������ƣ�������ģ��Ч�����ٶ���ȡ�ᣡ
class Sequence_Label_Priority_Combining_Statistical_Law_Rule(SPO_Generation_Rule_Base):

    def __init__(self, ):
        SPO_Generation_Rule_Base.__init__(self)
        self.spo_list_heuristic_generation = SPO_List_Heuristic_Generation()
        self.spo_predicate_temple = SPO_Predicate_Temple()

    # �������ʱʹ�ã���ʾָ����ϵ���
    def check_refer_spo_list_predicate(self, refer_spo_list, check_predicate_list):
        refer_predicate_list = [spo["predicate"] for spo in refer_spo_list]
        for predicate in check_predicate_list:
            if predicate in refer_predicate_list:
                return True
        return False

    # ���� spo_list ����  **����ӿں���**
    def rule_generate_spo_list(self, text_sentence, sort_relation_list, sort_entity_list, refer_spo_list, show_detail=False):
        def _combine_a_b_spo_list(spo_list_superset_A, spo_list_superset_B):
            spo_list_superset = []  # TODO:��д�����߼����������ֱ�Ӻϲ�
            for a in spo_list_superset_A:
                spo_list_superset.append(a)
            for b in spo_list_superset_B:
                spo_list_superset.append(b)
            return spo_list_superset

        # ����ģ��������� spo_list
        spo_list_superset_by_model_output = self.generate_spo_list_by_model_output(text_sentence, sort_relation_list, sort_entity_list)
        # ��������֪ʶ���� spo_list
        if len(spo_list_superset_by_model_output) == 0:
            spo_list_superset_by_key_word = self.generate_spo_list_only_by_priori_information(text_sentence)
            # �ϲ���ͬ�������ɵ� spo_list
            spo_list_superset = _combine_a_b_spo_list(spo_list_superset_by_model_output, spo_list_superset_by_key_word)
        else:
            spo_list_superset = spo_list_superset_by_model_output
        # �� spo_list �������м�֦
        spo_list = self.prune_spo_list_superset_and_change_order(spo_list_superset)
        #show_predicate_flag = self.check_refer_spo_list_predicate(refer_spo_list, ['���', '�˿�����'] )
        show_predicate_flag = False
        if show_predicate_flag and random.random()> 0.7 :
            print("text_sentence:        ", text_sentence)
            print("sort_relation_list:   ", sort_relation_list)
            print("sort_entity_list:     ", sort_entity_list)
            print("-"*100)
            print("refer_spo_list:       ", refer_spo_list)
            #print("spo_list_superset_A:   ", spo_list_superset_by_model_output)
            #print("spo_list_superset_B:   ", spo_list_superset_by_key_word)
            print("spo_list:             ", spo_list)
            print("\n")

        return spo_list

    # ��������֪ʶ���ɺ�ѡ spo_list
    def generate_spo_list_only_by_priori_information(self, text_sentence):
        # TODO��Wait coding �ȴ���д����ͨ��������Ϣ����Ĺ�ϵ
        wait_relation_list = ["�ܲ��ص�", "Ŀ", "���", "��ӳʱ��", "����ר��", "ע���ʱ�", "�׶�", "���",
                            "��Ʒ��˾", "��ҵ����", "��������", "����", "����", "������վ", "����", "������",
                            "רҵ����", "����", "��ҵԺУ", "ռ�����", "�ٷ�����", "��������",
                            "���ڳ���", "����", "����", "�ı���"]
        # �Ѿ�����ͨ��������Ϣ����Ĺ�ϵ
        relation_list = ["�漮", "������", "���³�", "��ʼ��", "������", "�α�", '���', '�˿�����',
                        '��', '����', '��', '����', '����', '����', '����', '����', 'ĸ��', '�ɷ�',
                         '����', '��Ƭ��', '���', '����', "��������"]
        spo_list_by_priori_info = []
        for relation_name in relation_list:
                spo_list_by_temple = self.spo_predicate_temple.temple_priori_information(relation_name, text_sentence)
                spo_list_by_priori_info.extend(spo_list_by_temple)
        return spo_list_by_priori_info

    #����ģ��������ɺ�ѡ spo_list
    def generate_spo_list_by_model_output(self, text_sentence, sort_relation_list, sort_entity_list):
        spo_list = []
        # �������� ('Number', '������'): ['���', '�˿�����'], ����
        mianji_spo_list, sort_relation_list = self.handle_mianji_renkoushuliang_problem(text_sentence, sort_relation_list, sort_entity_list)
        spo_list.extend(mianji_spo_list)
        #spo_list.extend(mianji_spo_list)
        # �������� ('����', '��������'): ['������', '�α�'], ����
        sort_relation_list = self.handle_zhuchiren_jiabin_problem(text_sentence, sort_relation_list, sort_entity_list)
        # �������� ('����', '��ҵ'): ['���³�', '��ʼ��'], ����
        sort_relation_list = self.handle_dongshizhang_chuangshiren_problem(text_sentence, sort_relation_list, sort_entity_list)
        # �������� ('�ص�', '����'): ['�漮', '������'],����
        sort_relation_list = self.handle_zuji_chushengdi_problem(text_sentence, sort_relation_list, sort_entity_list)
        # �������� ('����', '����'): ['����', '����', 'ĸ��', '�ɷ�'] ����
        renwu_renwu_problem_spo_list, sort_relation_list = self.handle_renwu_renwu_problem(text_sentence, sort_relation_list, sort_entity_list)
        spo_list.extend(renwu_renwu_problem_spo_list)
        # ʹ������֪ʶ������ϵ�б�
        sort_relation_list = self.use_prior_knowledg_adjustment_relationships(sort_relation_list, text_sentence)
        # ����ģ������Ĺ�ϵΪ�����б�
        relation_positive_list, relation_negative_list = self._split_relationship_by_score(sort_relation_list)
        # ��������ϵΪ ��\���� ��ϵ
        relation_positive_single_list, relation_positive_multiple_list = \
            self._split_relationship_by_single_or_multiple(relation_positive_list)
        # ������ϵ
        spo_list_by_single = self.handle_single_relation(text_sentence, relation_positive_single_list, sort_entity_list)
        spo_list.extend(spo_list_by_single)
        # ������ع�ϵ
        spo_list_by_grouping_form = self.handle_multiple_relations_in_grouping_form(
            text_sentence, relation_positive_multiple_list, sort_entity_list)
        spo_list.extend(spo_list_by_grouping_form)
        return spo_list

    def handle_mianji_renkoushuliang_problem(self, text_sentence, sort_relation_list, sort_entity_list):
        #�ں�ѡ���б� candidate_word_list ���ҳ��������Ĵ� center_word ����Ĵ���
        def find_word_B_nearest_to_word_A_for_single_relation(text_sentence, center_word, candidate_word_list):
            candidate_word_list_distance = []
            if center_word in text_sentence:
                word_A_index = text_sentence.index(center_word) + len(center_word) / 2
                candidate_word_list.reverse()  # �б�˳����Ϊ�˵����������ʾ������Ĵ���ͬ����ʱ�����ȷ����ұߵĵ���
            else:
                word_A_index = 0
            for candidate_word in candidate_word_list:
                if candidate_word in text_sentence:
                    candidate_word_index = text_sentence.index(candidate_word) + len(candidate_word) / 2
                else:
                    candidate_word_index = 1000
                candidate_word_list_distance.append(abs(candidate_word_index - word_A_index))
            if len(candidate_word_list_distance) > 0 :
                nearest_word = candidate_word_list[candidate_word_list_distance.index(min(candidate_word_list_distance))]
                return nearest_word
            else:
                return ""
        spo_list = []
        relation_list_new = []
        is_mianji_ren_kou_problem = False
        is_mianji_problem = False
        is_renkou_problem = False
        for relation_name, relation_value in sort_relation_list:
            if relation_name == "���" or relation_name == "�˿�����":
                relation_list_new.append((relation_name, 0.0))
            relation_list_new.append((relation_name, relation_value))
        for relation_name, relation_value in sort_relation_list:
            if relation_name in ["���", "�˿�����"] and relation_value > 0.5:
                is_mianji_ren_kou_problem = True
        for mianji_feature_word in ["���", "����", "ƽ��ǧ��", "ƽ������", "Ķ"]:
            if mianji_feature_word in text_sentence:
                is_mianji_problem = True
                break
        for renkou_feature_word in ["�˿�����", "�˿�", "����", "����"]:
            if renkou_feature_word in text_sentence:
                is_renkou_problem = True
                break
        if is_mianji_ren_kou_problem or is_mianji_problem or is_renkou_problem:
            xingzhengqu_list = self.spo_predicate_temple.get_entity_value_list_by_name("������", sort_entity_list)
            Number_list = self.spo_predicate_temple.get_entity_value_list_by_name("Number", sort_entity_list)
            if len(xingzhengqu_list) == 1:
                xingzhengqu = xingzhengqu_list[0]
                for Number in Number_list[:]:
                    if "��" in Number:
                        spo_item = self.spo_predicate_temple.create_new_spo_item("�˿�����", 'Number', '������', Number, xingzhengqu)
                        spo_list.append(spo_item)
                        Number_list.remove(Number)
                    else:
                        for mianji_feature_word in ["����", "ƽ��", "Ķ"]:
                            if mianji_feature_word in Number:
                                spo_item = self.spo_predicate_temple.create_new_spo_item("���", 'Number', '������', Number, xingzhengqu)
                                spo_list.append(spo_item)
                                Number_list.remove(Number)
                                break
                if len(Number_list) > 0:
                    for Number in Number_list:
                        flag = find_word_B_nearest_to_word_A_for_single_relation(text_sentence, Number, ["��", "���"])
                        if flag == "��" and "ƽ��" not in Number:
                            spo_item = self.spo_predicate_temple.create_new_spo_item("�˿�����", 'Number', '������', Number, xingzhengqu)
                            spo_list.append(spo_item)
                        else:
                            if "��" not in Number:
                                spo_item = self.spo_predicate_temple.create_new_spo_item("���", 'Number', '������', Number, xingzhengqu)
                                spo_list.append(spo_item)
        if len(spo_list) == 0:
            for relation_name in ["�˿�����", "���"]:
                spo_list.extend(self.spo_predicate_temple.temple_priori_information(relation_name, text_sentence))
        return spo_list, relation_list_new

    def handle_zhuchiren_jiabin_problem(self, text_sentence, sort_relation_list, sort_entity_list):
        change_flag = False
        relation_list_new = []
        for (relation_name, relation_value) in sort_relation_list[:]:
            if relation_name in ["������", "�α�"] and relation_value < 0.5:
                location_relation_word = self.spo_list_heuristic_generation.relational_location_word[relation_name]
                for location_word in location_relation_word:
                    if location_word in text_sentence:
                        relation_list_new.append((relation_name, 0.9))
                        change_flag = True
                        break
            else:
                relation_list_new.append((relation_name, relation_value))
        if change_flag:
            relation_list_new = sorted(relation_list_new, key=lambda x: x[1], reverse=True)
            return relation_list_new
        else:
            return sort_relation_list

    def handle_dongshizhang_chuangshiren_problem(self, text_sentence, sort_relation_list, sort_entity_list):
        change_flag = False
        relation_list_new = []
        for relation_name, relation_value in sort_relation_list:
            if relation_name in ["���³�", "��ʼ��"] and relation_value < 0.5:
                location_relation_word = self.spo_list_heuristic_generation.relational_location_word[relation_name]
                for location_word in location_relation_word:
                    if location_word in text_sentence:
                        relation_list_new.append((relation_name, 0.9))
                        change_flag = True
                        break
            else:
                relation_list_new.append((relation_name, relation_value))
        if change_flag:
            relation_list_new = sorted(relation_list_new, key=lambda x: x[1], reverse=True)
            return relation_list_new
        else:
            return sort_relation_list

    #����( '�ص�', '����'): ['�漮', '������'], ����
    def handle_zuji_chushengdi_problem(self, text_sentence, sort_relation_list, sort_entity_list):
        change_flag = False
        relation_list_new = []
        for relation_name, relation_value in sort_relation_list:
            if relation_name == "�漮" and "�漮" in text_sentence and relation_value < 0.5:
                relation_list_new.append((relation_name, 0.9))
                change_flag = True
            else:
                relation_list_new.append((relation_name, relation_value))

        if change_flag:
            relation_list_new = sorted(relation_list_new, key=lambda x: x[1], reverse=True)
            return relation_list_new
        else:
            return sort_relation_list

    # ���� ('����', '����'): ['����', '����', 'ĸ��', '�ɷ�'] ����
    def handle_renwu_renwu_problem(self, text_sentence, sort_relation_list, sort_entity_list):
        spo_list = []
        is_renwu_renwu_problem = False
        renwu_entity_number = 0
        ren_ren_problem_possibility_dict = dict()
        # ��ȡ['����', '����', 'ĸ��', '�ɷ�']�����Դ�С
        for relation, value in sort_relation_list:
            if relation in ['����', '����', 'ĸ��', '�ɷ�']:
                ren_ren_problem_possibility_dict[relation] = value

        for entity_name, entity_value in sort_entity_list:
            if entity_name == "����":
                renwu_entity_number += 1

        if renwu_entity_number >= 2:
            for item in sort_relation_list[0:4]: #ֻ�鿴�����ϵ�б��ǰ��λȷ���Ƿ�Ϊ renwu_renwu_problem
                relation, value = item
                if relation in ['����', '����', 'ĸ��', '�ɷ�']:
                    sort_relation_list.remove(item)
                    is_renwu_renwu_problem = True

        # ('����', '����'): ['����', '����', 'ĸ��', '�ɷ�'],
        def heuristic_generate_fuqin_muqin_zhangfu_qizi(text_sentence, ren_ren_problem_possibility_dict, sort_entity_list):
            spo_list = []
            greater_flag = False
            for relation, value in ren_ren_problem_possibility_dict.items():
                if value > 0.5:
                    spo_list.extend(self.spo_predicate_temple.temple_priori_information(relation, text_sentence))
                    # print("@@heuristic_generate_fuqin_muqin_zhangfu_qizi������֪ʶ��ȡ",
                    #       self.spo_predicate_temple.temple_priori_information(relation, text_sentence))
                    greater_flag = True
            if greater_flag == False:
                for relation, value in ren_ren_problem_possibility_dict.items():
                    spo_list.extend(self.spo_predicate_temple.temple_priori_information(relation, text_sentence))
            return spo_list
        if is_renwu_renwu_problem:
            spo_list = heuristic_generate_fuqin_muqin_zhangfu_qizi(text_sentence, ren_ren_problem_possibility_dict, sort_entity_list)
        return spo_list, sort_relation_list

    # ������ϵ
    def handle_single_relation(self, text_sentence, relation_positive_single_list, sort_entity_list):
        #�ں�ѡ���б� candidate_word_list ���ҳ��������Ĵ� center_word ����Ĵ���
        def find_word_B_nearest_to_word_A_for_single_relation(text_sentence, center_word, candidate_word_list):
            candidate_word_list_distance = []
            if center_word in text_sentence:
                word_A_index = text_sentence.index(center_word) + len(center_word) / 2
                candidate_word_list.reverse()  # �б�˳����Ϊ�˵����������ʾ������Ĵ���ͬ����ʱ�����ȷ����ұߵĵ���
            else:
                word_A_index = 0
            for candidate_word in candidate_word_list:
                if candidate_word in text_sentence:
                    candidate_word_index = text_sentence.index(candidate_word) + len(candidate_word) / 2
                else:
                    candidate_word_index = 1000
                candidate_word_list_distance.append(abs(candidate_word_index - word_A_index))
            if len(candidate_word_list_distance) > 0 :
                nearest_word = candidate_word_list[candidate_word_list_distance.index(min(candidate_word_list_distance))]
                return nearest_word
            else:
                return ""

        spo_list = []
        if len(sort_entity_list) <= 1:
            return []
        if len(sort_entity_list) == 2:
            for relation_name in relation_positive_single_list:
                spo_list_by_temple_one = self.spo_predicate_temple.temple_one(relation_name, sort_entity_list)
                spo_list.extend(spo_list_by_temple_one)
        else:
            for relation_name in relation_positive_single_list:
                subject_type = self.schemas_dict_relation_2_subject_object[relation_name][0][0]
                object_type = self.schemas_dict_relation_2_subject_object[relation_name][0][1]
                subject_value_list = self.spo_predicate_temple.get_entity_value_list_by_name(subject_type, sort_entity_list)
                object_value_list = self.spo_predicate_temple.get_entity_value_list_by_name(object_type, sort_entity_list)
                subject_value_list_len = len(subject_value_list)
                object_value_list_len = len(object_value_list)
                if relation_name in ['������', '�α�']: #('����', '��������'): ['������', '�α�'],
                    for subject_value in subject_value_list:
                        object_value = find_word_B_nearest_to_word_A_for_single_relation(text_sentence, subject_value,
                                                                                         object_value_list)
                        spo_item = self.spo_predicate_temple.create_new_spo_item(relation_name, subject_type,
                                                                                 object_type, subject_value,
                                                                                 object_value)
                        spo_list.append(spo_item)
                else:
                    if object_value_list_len <= subject_value_list_len:
                        for object_value in object_value_list:
                            subject_value = find_word_B_nearest_to_word_A_for_single_relation(text_sentence, object_value, subject_value_list)
                            spo_item = self.spo_predicate_temple.create_new_spo_item(relation_name, subject_type, object_type, subject_value,
                                                                object_value)
                            spo_list.append(spo_item)
                    else:
                        for subject_value in subject_value_list:
                            object_value = find_word_B_nearest_to_word_A_for_single_relation(text_sentence, subject_value, object_value_list)
                            spo_item = self.spo_predicate_temple.create_new_spo_item(relation_name, subject_type, object_type, subject_value,
                                                                object_value)
                            spo_list.append(spo_item)
        return spo_list

    # �÷���İ취������ع�ϵ
    def handle_multiple_relations_in_grouping_form(self, text_sentence, relation_positive_multiple_list, sort_entity_list):
        def split_form_relation_by_one_zero_flag(need_analysis_relation_flag_dict):
            need_analysis_relation_list = [relation for relation, flag in need_analysis_relation_flag_dict.items() if flag == 1]
            return need_analysis_relation_list

        spo_list = []
        if len(sort_entity_list) <= 1:
            return []
        # ���ϵ����
        form_zuji_chushengdi = ["�漮", "������"]
        form_dongshizhang_chuangshiren = ["���³�", "��ʼ��"]
        form_zhuchiren_jiabin = ["������", "�α�"]
        form_mianji_renkoushuliang = ['���', '�˿�����']
        form_zi_chaodai_hao = ['��', '����', '��']
        form_geshou_zuoci_zuoqu = ['����', '����', '����']
        form_daoyan_zhipianren_bianju_zhuyan = ['����', '��Ƭ��', '���', '����']
        multiple_relations_in_group_list = [form_zuji_chushengdi, form_dongshizhang_chuangshiren, form_zhuchiren_jiabin,
                                            form_mianji_renkoushuliang, form_zi_chaodai_hao, form_geshou_zuoci_zuoqu,
                                            form_geshou_zuoci_zuoqu, form_daoyan_zhipianren_bianju_zhuyan]
        # �������ʽ�������ع�ϵ�б�
        for multiple_relations_form in multiple_relations_in_group_list:
            need_analysis_relation_flag_dict = dict()
            for relation in multiple_relations_form:
                if relation in relation_positive_multiple_list:
                    need_analysis_relation_flag_dict[relation] = 1
                else:
                    need_analysis_relation_flag_dict[relation] = 0
            need_analysis_relation_list = split_form_relation_by_one_zero_flag(need_analysis_relation_flag_dict)
            # ���ֻ��һ����ϵ����Ȼ�õ���ϵ����취 TODO:���['����', '��Ƭ��', '���', '����']����ʹ�ǵ���ϵҲӦ��ʹ�ò�ͬ�Ĵ�����������Ľ�
            if len(need_analysis_relation_list) == 1:
                spo_list.extend(self.handle_single_relation(text_sentence, need_analysis_relation_list, sort_entity_list))
            # ������ж����ϵ����������ʽ����취
            elif len(need_analysis_relation_list) > 1:
                spo_list.extend(self.spo_list_heuristic_generation.heuristic_handle_multiple_relations(
                    text_sentence, need_analysis_relation_flag_dict, sort_entity_list))
        # ���ϵ�����־
        form_zuji_chushengdi_flag = False
        form_dongshizhang_chuangshiren_flag = False
        form_zhuchiren_jiabin_flag = False
        form_mianji_renkoushuliang_flag = False
        form_zi_chaodai_hao_flag = False
        form_geshou_zuoci_zuoqu_flag = False
        form_fuqin_muqin_zhangfu_qizi_flag = False
        form_daoyan_zhipianren_bianju_zhuyan_flag = False

        for relation in relation_positive_multiple_list:
            if relation in form_zuji_chushengdi:
                form_zuji_chushengdi_flag = True
            if relation in form_dongshizhang_chuangshiren:
                form_dongshizhang_chuangshiren_flag = True
            if relation in form_zhuchiren_jiabin:
                form_zhuchiren_jiabin_flag = True
            if relation in form_mianji_renkoushuliang:
                form_mianji_renkoushuliang_flag = True
            if relation in form_zi_chaodai_hao:
                form_zi_chaodai_hao_flag = True
            if relation in form_geshou_zuoci_zuoqu:
                form_geshou_zuoci_zuoqu_flag = True
            if relation in form_daoyan_zhipianren_bianju_zhuyan:
                form_daoyan_zhipianren_bianju_zhuyan_flag = True

        return spo_list

    # �����ɵ��б���м�֦
    def prune_spo_list_superset_and_change_order(self, spo_list_superset, show_details=False):
        spo_list = []
        spo_list_superset_tuple = set()
        for spo in spo_list_superset:
            spo_list_superset_tuple.add(tuple((k, v) for k, v in spo.items()))
        for spo in spo_list_superset_tuple:
            spo_list.append(dict(spo))
        spo_list_ordered = []
        for spo in spo_list:
            spo_object_type = spo["object_type"]
            spo_predicate = spo["predicate"]
            spo_object = spo["object"]
            spo_subject_type = spo["subject_type"]
            spo_subject = spo["subject"]
            if len(spo_subject) > 0 and len(spo_object) > 0:
                spo_list_ordered.append({"predicate":spo_predicate,
                                         "object_type":spo_object_type, "subject_type":spo_subject_type,
                                         "object":spo_object, "subject":spo_subject, })
            else:
                #print("$$��֦prune_spo_list_superset_and_change_order", spo)
                pass

        if show_details and (len(spo_list) < len(spo_list_superset)):
            print("prune_spo_list_superset...")
            print(len(spo_list), len(spo_list_superset))
            print(spo_list)
            print(spo_list_superset)
            print("\n")
        return spo_list_ordered

    # ʹ������֪ʶ������ϵ�б�
    def use_prior_knowledg_adjustment_relationships(self, sort_relation_list, text_sentence):
        # combine_relation_list = self.distinguishing_zu_ji_and_chu_sheng_di_relation(combine_relation_list, text_sentence)
        # combine_relation_list = self.distinguishing_chuang_shi_ren_and_dong_shi_zhang(combine_relation_list, text_sentence)
        # combine_relation_list = self.distinguishing_zhu_chi_ren_and_jia_bin(combine_relation_list, text_sentence)
        # combine_relation_list = self.distinguishing_mian_ji_and_ren_kou_shu_liang(combine_relation_list, text_sentence)
        # combine_relation_list = self.distinguishing_zi_chao_dai_and_hao(combine_relation_list, text_sentence)
        # combine_relation_list = self.distinguishing_ge_shou_zuo_ci_and_zuo_qu(combine_relation_list, text_sentence)
        # combine_relation_list = self.distinguishing_fu_qin_mu_qin_zhang_fu_and_qi_zi(combine_relation_list, text_sentence)
        # combine_relation_list = self.distinguishing_dao_yan_zhi_pian_ren_bian_ju_and_zhu_yan(combine_relation_list, text_sentence)
        relation_list_new = []
        for (relation_name, relation_value) in sort_relation_list:
            if relation_name in ['����', '��Ƭ��', '���', '����']:
                change_Flag = False
                feature_word_list = self.spo_list_heuristic_generation.relational_location_word[relation_name]
                for feature_word in feature_word_list:
                    if feature_word in text_sentence and relation_value < 0.5:
                        change_Flag = True
                        break
                if change_Flag:
                    relation_list_new.append((relation_name, 0.7))
                else:
                    relation_list_new.append((relation_name, relation_value))
            else:
                relation_list_new.append((relation_name, relation_value))

        sort_relation_list_new = sorted(relation_list_new, key=lambda x: x[1], reverse=True)

        # if relation_list_new != sort_relation_list_new:
        #     print("@@����use_prior_knowledg_adjustment_relationships - sort_relation_list_new", sort_relation_list_new)
        #     print("@@����use_prior_knowledg_adjustment_relationships - sort_relation_list_old", sort_relation_list)
        return sort_relation_list_new

    # ���ģ�ͺ�����֪ʶԤ���ϵ
    def combine_model_output_and_priori_knowledge_prediction_relation(self, text_sentence, sort_relation_list, sort_entity_list):
        # ��ģ��ֱ������Ĺ�ϵ
        relation_positive_list, relation_negative_list = self._split_relationship_by_score(sort_relation_list)
        # ����ʵ�������б�
        subject_object_type_list = [name for name, value in sort_entity_list]
        # ��ʵ�������Ʋ��ϵ
        relation_infer_from_labeling_positive_list, relation_infer_from_labeling_supplement_list = self.subject_object_type_2_relation_list(subject_object_type_list)
        # �ɾ������������Ʋ��ϵ
        relation_feature_by_feature_word_list = []
        # ʹ������֪ʶ������ϵ�б�
        combine_relation_list = self.use_prior_knowledg_adjustment_relationships(relation_positive_list, text_sentence)
        # �ϲ�ģ��ֱ������Ĺ�ϵ����ʵ�������Ʋ�Ĺ�ϵ�������ʹ�ϵ�б�
        combine_relation_list = self._merge_possible_relation_list(relation_positive_list, relation_negative_list,
                                                                   relation_infer_from_labeling_positive_list,
                                                                   relation_infer_from_labeling_supplement_list,
                                                                   relation_feature_by_feature_word_list)
        # ȥ��
        combine_relation_list = list(set(combine_relation_list))
        return combine_relation_list

    # �ϲ��ɲ�ͬ;�������ı�ѡ��ϵ
    def _merge_possible_relation_list(self, relation_positive_list, relation_negative_list,
                                     relation_infer_from_labeling_positive_list, relation_infer_from_labeling_supplement_list,
                                      relation_feature_by_feature_word_list, guaranteed_not_empty_relation_list=False):
        # �ϲ�ģ��ֱ�����������ϵ����ʵ�������Ʋ��������ϵ
        combine_relation_list = list(set(relation_positive_list) | set(relation_infer_from_labeling_positive_list))
        # �ϲ������ʹ�ϵ�б�
        combine_relation_list = list(set(combine_relation_list) | set(relation_feature_by_feature_word_list))
        # ���������ȻΪ�գ��� guaranteed_not_empty_relation_list = True�������ʹ��ģ��ֱ�������Ը������Ĺ�ϵ������<0.5��
        if guaranteed_not_empty_relation_list and len(combine_relation_list) == 0:
            combine_relation_list.append(relation_negative_list[0])
        return combine_relation_list

    # ��ʵ�������Ʋ���ܹ�ϵ
    def subject_object_type_2_relation_list(self, subject_object_type_list):
        #��ʵ���Ƴ��ĵ���ϵ������('�ص�', '��ҵ')--> ['�ܲ��ص�'],  ����ϵ�б�
        relation_infer_from_labeling_positive_list = []
        #��ʵ���Ƴ��Ķ��ϵ������('����', '����')-->['����', '����', '����']�����������ᵼ�¶�������ϵ���������֣����Խ���������ο�
        relation_infer_from_labeling_supplement_list = []
        # ���ݶ��ʵ�����͵ĸ������������ܵĹ�ϵ��
        if len(subject_object_type_list) >= 2:
            subject_object_type_permutations = permutations(subject_object_type_list, 2)
            lawful_subject_object_type_tuple_list = [
                subject_object for subject_object in subject_object_type_permutations
                if subject_object in self.schemas_dict_subject_object_2_relation]
            relation_infer_from_labeling_positive_list = list()
            for subject_object in lawful_subject_object_type_tuple_list:
                if subject_object not in [('�ص�', '����'), ('����', '��ҵ'), ('����', '��������'),
                                          ('Number', '������'), ('Text', '��ʷ����'), ('����', '����'),
                                          ('����', '����'), ('����', 'Ӱ����Ʒ')]:
                    relation_infer_from_labeling_positive_list.extend(self.schemas_dict_subject_object_2_relation[subject_object])
                else:
                    relation_infer_from_labeling_supplement_list.extend(self.schemas_dict_subject_object_2_relation[subject_object])
        return relation_infer_from_labeling_positive_list, relation_infer_from_labeling_supplement_list

if __name__=='__main__':
    sorted_relation_and_entity_list = Sorted_relation_and_entity_list_Management(TEST_DATA_DIR="../data/SKE_2019/test", MODEL_OUTPUT_DIR="../output/20190319code_test", Competition_Mode=False)
    relation_first_rule = Relationship_Priority_Rule()





