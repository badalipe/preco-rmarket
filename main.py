import requests
from bs4 import BeautifulSoup
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    GmsBarcodeScanning = autoclass('com.google.mlkit.vision.codescan.GmsBarcodeScanning')
    BuilderOptions = autoclass('com.google.mlkit.vision.codescan.GmsBarcodeScannerOptions$Builder')
    Barcode = autoclass('com.google.mlkit.vision.barcode.common.Barcode')

class PriceCheckerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        self.label_status = Label(
            text='Toque no botão para ler o código de barras',
            font_size=18,
            halign='center'
        )
        self.layout.add_widget(self.label_status)
        
        self.btn_scan = Button(
            text='Escanear Código de Barras',
            font_size=20,
            size_hint=(1, 0.3),
            background_color=(0.1, 0.6, 0.9, 1)
        )
        self.btn_scan.bind(on_press=self.start_scanner)
        self.layout.add_widget(self.btn_scan)
        
        return self.layout

    def start_scanner(self, instance):
        if platform == 'android':
            try:
                activity = PythonActivity.mActivity
                options_builder = BuilderOptions()
                options = options_builder.setBarcodeFormats(
                    Barcode.FORMAT_EAN_13,
                    Barcode.FORMAT_EAN_8,
                    Barcode.FORMAT_UPC_A
                ).build()
                
                scanner = GmsBarcodeScanning.getClient(activity, options)
                task = scanner.startScan()
                task.addOnSuccessListener(self.on_scan_success)
                task.addOnFailureListener(self.on_scan_failure)
            except Exception as e:
                self.label_status.text = f'Erro ao abrir o leitor: {str(e)}'
        else:
            # Simulação para testes em ambiente de desenvolvimento (PC)
            self.consultar_preco("1574")

    def on_scan_success(self, barcode):
        if barcode:
            raw_value = barcode.getRawValue()
            self.label_status.text = f'Código lido: {raw_value}\nA consultar preço...'
            self.consultar_preco(raw_value)

    def on_scan_failure(self, exception):
        self.label_status.text = f'Falha no leitor: {exception.getMessage()}'

    def consultar_preco(self, codigo_barras):
        base_url = 'https://rmarket.cartazfacil.pro'
        
        try:
            # Mantém a sessão HTTP para gerir os cookies de autenticação
            session = requests.Session()
            
            # 1. Autenticação inicial com as credenciais fornecidas
            login_data = {
                'usuario': 'rmarket07',
                'senha': 'sup12345'
            }
            session.post(f'{base_url}/index.php', data=login_data, allow_redirects=True)
            
            # 2. Consulta direta através do endpoint de busca mapeado nos registos
            search_url = f'{base_url}/inc/buscaProduto.php'
            search_data = {
                'buscaProd': codigo_barras,
                'sessao': ''
            }
            search_res = session.post(search_url, data=search_data)
            
            if search_res.status_code == 200:
                soup = BeautifulSoup(search_res.text, 'html.parser')
                
                # Exemplo de extração: Localizar os dados do produto na resposta HTML
                # Dependendo do formato exato retornado pelo buscaProduto.php, 
                # podemos puxar a descrição e o ID para o passo seguinte de preço.
                texto_resposta = soup.get_text(strip=True)
                
                if len(texto_resposta) > 10:
                    self.label_status.text = f'Produto Encontrado!\nCódigo: {codigo_barras}\n(Dados carregados com sucesso)'
                    
                    # Opcional: Se precisar do preço exato da tabela de valores, 
                    # pode encadear a chamada ao endpoint de preços identificado nos logs:
                    # id_produto = "..." # extraído do HTML de busca
                    # preco_res = session.get(f'{base_url}/inc/filtro_select.php?ref=valorProd&id_produto={id_produto}')
                else:
                    self.label_status.text = f'Nenhum produto encontrado para: {codigo_barras}'
            else:
                self.label_status.text = 'Erro ao comunicar com o servidor do Cartaz Fácil.'
                
        except Exception as e:
            self.label_status.text = f'Erro na requisição: {str(e)}'

if __name__ == '__main__':
    PriceCheckerApp().run()
