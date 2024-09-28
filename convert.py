import xml.etree.ElementTree as ET
from xml.dom import minidom
import csv
import datetime

def csv_to_opml(input_file, output_file, title):
    # 创建OPML结构
    opml = ET.Element('opml', version='1.0')
    head = ET.SubElement(opml, 'head')
    ET.SubElement(head, 'title').text = title
    ET.SubElement(head, 'dateCreated').text = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
    body = ET.SubElement(opml, 'body')

    # 读取CSV文件并创建OPML结构
    categories = {}
    with open(input_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # 跳过标题行
        for row in reader:
            category, text_title, rss_link =  row

            if category not in categories:
                categories[category] = ET.SubElement(body, 'outline', text=category, title=category)

            outline = ET.SubElement(categories[category], 'outline')
            outline.set('text', text_title)
            outline.set('title', text_title)
            outline.set('type', 'rss')
            outline.set('xmlUrl', rss_link)

    # 生成漂亮的XML
    xml_str = minidom.parseString(ET.tostring(opml)).toprettyxml(indent='  ')

    # 写入OPML文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_str)

# 使用示例
if __name__ == "__main__":
    csv_to_opml('rss_links.csv', 'subscriptions.opml', 'My RSS Subscriptions')
    print("OPML file has been generated successfully.")