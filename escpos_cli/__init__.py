"""Main module."""
import logging
import argparse

from xmlescpos.printer import Usb
from xmlescpos.exceptions import NoStatusError


logger = logging.getLogger(__name__)
__VERSION__ = '0.0.2'


def main():
    """Main function."""
    def auto_int(x):
        """Convert a string to int with auto base detection."""
        return int(x, 0)

    parser = argparse.ArgumentParser(prog='escpos-cli', description='%(prog)s is a command-line utility for printing stuff using pyxmlescpos')
    parser.add_argument('-dvid', '--device-vendor-id', required=True, type=auto_int)
    parser.add_argument('-dpid', '--device-product-id', required=True, type=auto_int)
    parser.add_argument('-di', '--device-interface', type=int, default=0)
    parser.add_argument('-die', '--device-input-endpoint', type=auto_int, default=0x82)
    parser.add_argument('-doe', '--device-output-endpoint', type=auto_int, default=0x01)
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-o', '--open-cashdrawer', action='store_true')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __VERSION__)
    parser.add_argument('receipt_xml', type=str)
    args = parser.parse_args()

    device = Usb(
        args.device_vendor_id,
        args.device_product_id,
        interface=args.device_interface,
        in_ep=args.device_input_endpoint,
        out_ep=args.device_output_endpoint
    )

    try:
        device.get_printer_status()
    except NoStatusError as e:
        logger.error(e)
    except Exception as e:
        logger.error("An unknown exception occured: " + str(e))
    else:
        if args.open_cashdrawer:
            device.cashdraw(2)
            device.cashdraw(5)

        if args.receipt_xml:
            device.receipt(args.receipt_xml)



if __name__ == '__main__':
    """Standard import guard."""
    main()
