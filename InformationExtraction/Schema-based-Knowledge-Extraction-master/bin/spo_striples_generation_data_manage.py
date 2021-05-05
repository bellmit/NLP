#coding=gbk
import os

class File_Management(object):
    """��ȡTXT�ļ������б���ʽ�����ļ�����"""
    def __init__(self, TEST_DATA_DIR= None, MODEL_OUTPUT_DIR=None, RAW_DATA_DIR=None, Competition_Mode=False):
        self.TEST_DATA_DIR = TEST_DATA_DIR
        self.MODEL_OUTPUT_DIR = MODEL_OUTPUT_DIR
        self.RAW_DATA_DIR = RAW_DATA_DIR
        self.Competition_Mode = Competition_Mode

    def file_path_and_name(self):
        text_sentence_file_path = os.path.join(self.TEST_DATA_DIR, "text.txt")
        token_in_file_path = os.path.join(self.TEST_DATA_DIR, "token_in_not_UNK.txt")
        # Ϊ�˱��������� relationship ���� prediction ���� predicate ��ʾģ�͵����
        predicate_relationship_file_path = os.path.join(self.MODEL_OUTPUT_DIR, "SPO_predicate_test_results.txt")
        predicate_token_label_file_path = os.path.join(self.MODEL_OUTPUT_DIR, "token_label_prediction_test_results.txt")

        file_path_list = [text_sentence_file_path, token_in_file_path,
                          predicate_relationship_file_path, predicate_token_label_file_path]
        file_name_list = ["text_sentence_list", "token_in_not_NUK_list ",
                          "predicate_relationship_list", "predicate_token_label_list",]
        if not self.Competition_Mode:
            spo_out_file_path = os.path.join(self.TEST_DATA_DIR, "spo_out.txt")
            file_path_list.append(spo_out_file_path)
            file_name_list.append("reference_spo_list")
        return file_path_list, file_name_list

    def read_file_return_content_list(self):
        file_path_list, file_name_list = self.file_path_and_name()
        content_list_summary = []
        for file_path in file_path_list:
            with open(file_path, "r", encoding='utf-8') as f:
                content_list = f.readlines()
                content_list = [content.replace("\n", "") for content in content_list]
                content_list_summary.append(content_list)
        content_list_length_summary = [(file_name, len(content_list)) for content_list, file_name in
                                       zip(content_list_summary, file_name_list)]
        file_line_number = self._check_file_line_numbers(content_list_length_summary)
        return content_list_summary, file_line_number

    def _check_file_line_numbers(self, content_list_length_summary):
        content_list_length_file_one = content_list_length_summary[0][1]
        for file_name, file_line_number in content_list_length_summary:
            assert file_line_number == content_list_length_file_one
        return content_list_length_file_one


class Sorted_relation_and_entity_list_Management(File_Management):
    """
    ���ɰ����ʴ�С����Ŀ��ܹ�ϵ�б�Ͱ���ԭʼ������˳�������ʵ���б�
    """
    def __init__(self, TEST_DATA_DIR= None, MODEL_OUTPUT_DIR=None, RAW_DATA_DIR=None, Competition_Mode=False):
        File_Management.__init__(self, TEST_DATA_DIR=TEST_DATA_DIR, MODEL_OUTPUT_DIR=MODEL_OUTPUT_DIR, RAW_DATA_DIR=RAW_DATA_DIR, Competition_Mode=Competition_Mode)
        # ��ϵ�б� ��ģ�������ʵ��ֵ��ӦΪ��ǩ
        self.relationship_label_list = ['�ɷ�', '��ӳʱ��', 'רҵ����', '������', '����', '����', '�˿�����', '����', '����', '����', '��ҵ����', '��Ʒ��˾', '������', '������', '��������', '��ʼ��', '��Ƭ��', 'ռ�����', '��', '�α�', '����', '����', '��', '�ٷ�����', '����', '�ܲ��ص�', '��������', '���ڳ���', '����ר��', '�ı���', '����', '����', 'ĸ��', '��ҵԺУ', '����', '����', 'ע���ʱ�', '����', '����', 'Ŀ', '�漮', '���', '���', '���³�', '���', '������վ', '��������', '���', '�׶�']

    def get_input_list(self,):
        content_list_summary, self.file_line_number = self.read_file_return_content_list()
        if self.Competition_Mode:
            reference_spo_list = [None] * self.file_line_number
            content_list_summary.append(reference_spo_list)

        [text_sentence_list, token_in_list, predicate_relationship_list, predicate_token_label_list,
            reference_spo_list] = content_list_summary
        return text_sentence_list, token_in_list, predicate_relationship_list, predicate_token_label_list, reference_spo_list

    # ��ģ������Ĺ�ϵ���տ����Դ�С����Ȼ������������б�
    def model_predicate_relationship_2_sort_list(self, predicate_relationship_list):
        relationship_dict = dict()
        for relationship_value, relationship_label in zip(predicate_relationship_list, self.relationship_label_list):
            relationship_dict[relationship_label] = float(relationship_value)
        relationship_dict = sorted(relationship_dict.items(), key=lambda x: x[1], reverse=True)
        return relationship_dict

    # ��ȥģ��������������
    def _preprocessing_model_token_lable(self, predicate_token_label_list):

        predicate_token_label_list = predicate_token_label_list[1:-1]  # y_predict.remove('[CLS]') #y_predict.remove('[SEP]')
        #ToDo:�����󣬾���
        return predicate_token_label_list

    #�ϲ���WordPiece�зֵĴʺ͵���
    def _merge_WordPiece_and_single_word(self, entity_sort_list):
        # [..['B-����ר��', '��', '��', '��', 'ge', '##nes', '##is'] ..]---> [..('����ר��', '�µ���genesis')..]
        entity_sort_tuple_list = []
        for a_entity_list in entity_sort_list:
            entity_content = ""
            entity_type = None
            for idx, entity_part in enumerate(a_entity_list):
                if idx == 0:
                    entity_type = entity_part
                    if entity_type[:2] not in ["B-", "I-"]:
                        break
                else:
                    if entity_part.startswith("##"):
                        entity_content += entity_part.replace("##", "")
                    else:
                        entity_content += entity_part
            if entity_content != "":
                entity_sort_tuple_list.append((entity_type[2:], entity_content))
        return entity_sort_tuple_list

    # ��spo_out.txt ��[SPO_SEP] �ָ���ʽת���ɱ�׼�б��ֵ���ʽ
    # ���� ���� ���� ����� �ܷ�[SPO_SEP]�ɷ� ���� ���� �ܷ� ����� ---> dict
    def _preprocessing_reference_spo_list(self, refer_spo_str):
        refer_spo_list = refer_spo_str.split("[SPO_SEP]")
        refer_spo_list = [spo.split(" ") for spo in refer_spo_list]
        refer_spo_list = [dict([('predicate', spo[0]),
                                ('object_type', spo[2]), ('subject_type', spo[1]),
                                ('object', spo[4]), ('subject', spo[3])]) for spo in refer_spo_list]
        refer_spo_list.sort(key= lambda item:item['predicate'])
        return refer_spo_list

    # ��ģ�����ʵ���ǩ����ԭ�������λ�����
    def model_token_label_2_entity_sort_tuple_list(self, token_in_not_UNK, predicate_token_label):
        """
        :param token_in_not_UNK:  ['��', '��', '��', '��', '��', '��', 'Ŀ', '��', '��', '��', '��', '��', '��', '��', '��', '��', 'ֲ', '��']
        :param predicate_token_label: ['B-����', 'I-����', 'I-����', 'I-����', 'O', 'B-Ŀ', 'I-Ŀ', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
        :return: [('B-����', '�Ͼջ���'), ('B-Ŀ', '��Ŀ')]
        """
        token_in_not_UNK_list = token_in_not_UNK.split(" ")
        predicate_token_label_list = predicate_token_label.split(" ")
        predicate_token_label_list = self._preprocessing_model_token_lable(predicate_token_label_list)
        entity_sort_list = []
        entity_part_list = []
        #TODO:��Ҫ������µ��߼��жϣ�����д�Ĳ����걸���
        for idx, token_label in enumerate(predicate_token_label_list):
            # �����ǩΪ "O"
            if token_label == "O":
                # entity_part_list ��Ϊ�գ���ֱ���ύ
                if len(entity_part_list) > 0:
                    entity_sort_list.append(entity_part_list)
                    entity_part_list = []
            # �����ǩ���ַ� "B-" ��ʼ
            if token_label.startswith("B-"):
                # ��� entity_part_list ��Ϊ�գ������ύԭ�� entity_part_list
                if len(entity_part_list) > 0:
                    entity_sort_list.append(entity_part_list)
                    entity_part_list = []
                entity_part_list.append(token_label)
                entity_part_list.append(token_in_not_UNK_list[idx])
                # ������˱�ǩ�������һ����ǩ��
                if idx == len(predicate_token_label_list) - 1:
                    entity_sort_list.append(entity_part_list)
            # �����ǩ���ַ� "I-"  ��ʼ ���ߵ��� "[##WordPiece]"
            if token_label.startswith("I-") or token_label == "[##WordPiece]":
                # entity_part_list ��Ϊ�գ���Ѹñ�ǩ��Ӧ�����ݲ��� entity_part_list
                if len(entity_part_list) > 0:
                    entity_part_list.append(token_in_not_UNK_list[idx])
                    # ������˱�ǩ�������һ����ǩ��
                    if idx == len(predicate_token_label_list) - 1:
                        entity_sort_list.append(entity_part_list)
        entity_sort_tuple_list = self._merge_WordPiece_and_single_word(entity_sort_list)
        return entity_sort_tuple_list

    # ��� ��ǩ��ע�ĸ��ֿ�������������Ƿ���ʵ�����ű�ע���м�û�� "O" ���
    def check_token_label_out(self):
        text_sentence_list, token_in_not_UNK_list, predicate_relationship_list, predicate_token_label_list, reference_spo_list = self.get_input_list()

        for [text_sentence, token_in_not_UNK, predicate_relationship, predicate_token_label, refer_spo_str] in\
                zip(text_sentence_list, token_in_not_UNK_list, predicate_relationship_list, predicate_token_label_list, reference_spo_list):
            predicate_token_label_list = predicate_token_label.split(" ")
            predicate_token_label_list = self._preprocessing_model_token_lable(predicate_token_label_list)
            #print(predicate_token_label_list)
            special_B = 0
            for item in predicate_token_label_list:
                if item == "O":
                    special_B = 0
                if item.startswith("B-"):
                    special_B += 1
                if special_B >= 2:
                    print(text_sentence)
                    print(refer_spo_str)
                    print(predicate_token_label_list)
                    print("\n")
                    break
            if special_B >= 2:
                break

    # ���� spo_list ��ԭ���е�����ʵ��λ�ú�������ϵ
    def analysis_position_quantity_relations_of_spo_list_in_text_sentence(self):
        def sentence_visualization(text_sentence, spo_list):
            count_so_type = set()
            for spo in spo_list:
                spo_predicate = spo['predicate']
                spo_subject_type = spo['subject_type']
                spo_object_type = spo['object_type']
                spo_subject = spo['subject']
                spo_object = spo['object']
                text_sentence = text_sentence.replace(spo_subject, " [({}){}] ".format(spo_subject_type, spo_subject))
                text_sentence = text_sentence.replace(spo_object, " [({}){}] ".format(spo_object_type, spo_object))
                print("({}, {}):[{}]".format(spo_subject_type, spo_object_type, spo_predicate))
                count_so_type.add(spo_subject_type)
                count_so_type.add(spo_object_type)
            print(text_sentence)

            print("\n")
            return count_so_type

        text_sentence_list, token_in_not_UNK_list, predicate_relationship_list, predicate_token_label_list, reference_spo_list = self.get_input_list()
        file_line_number = 0
        spo_list_line_two = 0
        so_type_number_dict = dict()
        for [text_sentence, token_in_not_UNK, predicate_relationship, predicate_token_label, refer_spo_str] in\
                zip(text_sentence_list, token_in_not_UNK_list, predicate_relationship_list, predicate_token_label_list, reference_spo_list):
            refer_spo_list = self._preprocessing_reference_spo_list(refer_spo_str)
            file_line_number += 1
            refer_spo_list_len = len(refer_spo_list)
            if refer_spo_list_len ==5:
                spo_list_line_two += 1
                count_so_type = sentence_visualization(text_sentence, refer_spo_list)
                #print("\n")
                so_type_number_dict[len(count_so_type)] = so_type_number_dict.setdefault(len(count_so_type), 0) + 1
        print(so_type_number_dict)
        print(spo_list_line_two, file_line_number, spo_list_line_two / file_line_number)

    # �����ź���Ĺ�ϵ�б��ʵ���б�
    def produce_relationship_and_entity_sort_list(self):
        text_sentence_list, token_in_not_UNK_list, predicate_relationship_list, predicate_token_label_list, reference_spo_list = self.get_input_list()

        for [text_sentence, token_in_not_UNK, predicate_relationship, predicate_token_label, refer_spo_str] in\
                zip(text_sentence_list, token_in_not_UNK_list, predicate_relationship_list, predicate_token_label_list, reference_spo_list):

            predicate_relationship_sort_list = self.model_predicate_relationship_2_sort_list(predicate_relationship.split())
            entity_sort_tuple_list = self.model_token_label_2_entity_sort_tuple_list(token_in_not_UNK, predicate_token_label)

            if self.Competition_Mode:
                yield text_sentence, predicate_relationship_sort_list, entity_sort_tuple_list, None
            else:
                refer_spo_list = self._preprocessing_reference_spo_list(refer_spo_str)
                yield text_sentence, predicate_relationship_sort_list, entity_sort_tuple_list, refer_spo_list

    # ��ӡ�ź���Ĺ�ϵ�б��ʵ���б�
    def show_produce_relationship_and_entity_sort_list(self):
        idx = 0
        for text_sentence, predicate_relationship_sort_list, entity_sort_tuple_list, refer_spo_list in self.produce_relationship_and_entity_sort_list():
            print("��ţ�           ", idx + 1)
            print("ԭ�䣺           ", text_sentence)
            print("Ԥ��Ĺ�ϵ��     ", predicate_relationship_sort_list)
            print("Ԥ���ʵ�壺     ", entity_sort_tuple_list)
            print("�ο��� spo_slit��", refer_spo_list)
            print("\n")
            idx += 1
            if idx == 10:
                break

if __name__=='__main__':
    sorted_relation_and_entity_list_manager = Sorted_relation_and_entity_list_Management(TEST_DATA_DIR="../data/SKE_2019/valid", MODEL_OUTPUT_DIR="../output/20190326code_test", Competition_Mode=False)
    sorted_relation_and_entity_list_manager.show_produce_relationship_and_entity_sort_list()
    #sorted_relation_and_entity_list_manager.check_token_label_out()
    #sorted_relation_and_entity_list_manager.analysis_position_quantity_relations_of_spo_list_in_text_sentence()
