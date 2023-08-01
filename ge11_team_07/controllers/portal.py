from odoo import http, _
from odoo.addons.portal.controllers import portal
from odoo.exceptions import AccessError, MissingError
from odoo.http import request

from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.osv.expression import OR


class PortalRepairOrder(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)

        RepairOrder = request.env["repair.order"]
        if "repair_count" in counters:
            values["repair_count"] = RepairOrder.search_count([])
            values["create_count"] = "New!"
        return values

    def _prepare_repair_order_portal_rendering_values(self, page=1, sortby=None, search_in="all", search=None, **kwargs):
        RepairOrder = request.env["repair.order"]

        domain = []
        url = "/repair-order/list"
        values = self._prepare_portal_layout_values()

        pager_values = portal_pager(
            url=url,
            total=RepairOrder.search_count(domain),
            page=page,
            step=self._items_per_page,
            url_args={"sortby": sortby,
                      "search_in": search_in, "search": search}
        )

        if search and search_in:
            domain += self._get_search_domain(search_in, search)

        registries = RepairOrder.search(
            domain, limit=self._items_per_page, offset=pager_values['offset'])

        values.update({
            "registries": registries.sudo(),
            "page_name": "repair_order",
            "pager": pager_values,
            "default_url": url,
            "search": search,
            "search_in": search_in,
            "sortby": sortby,
        })

        return values

    def _prepare_create_order_portal_rendering_values(self, page=1, sortby=None, search_in="all", search=None, **kwargs):
        RepairOrder = request.env["repair.order"]

        domain = []
        url = "/repair-order/list"
        values = self._prepare_portal_layout_values()

        pager_values = portal_pager(
            url=url,
            total=RepairOrder.search_count(domain),
            page=page,
            step=self._items_per_page,
            url_args={"sortby": sortby,
                      "search_in": search_in, "search": search}
        )

        if search and search_in:
            domain += self._get_search_domain(search_in, search)

        registries = RepairOrder.search(
            domain, limit=self._items_per_page, offset=pager_values['offset'])

        values.update({
            "registries": registries.sudo(),
            "page_name": "repair_order",
            "pager": pager_values,
            "default_url": url,
            "search": search,
            "search_in": search_in,
            "sortby": sortby,
        })

        return values

    @http.route("/repair-order/list", type="http", auth="user", website=True)
    def portal_my_repair_orders(self, **kwargs):
        values = self._prepare_repair_order_portal_rendering_values(
            **kwargs)
        return http.request.render("ge11_team_07.portal_my_repair_order_list", values)

    @http.route("/new-order/", type="http", auth="user", website=True)
    def portal_my_create_orders(self, **kwargs):
        values = self._prepare_create_order_portal_rendering_values(
            **kwargs)
        return http.request.render("ge11_team_07.portal_my_new_repair_order_list", values)

    @http.route(['/new-order/submit'], type='http', auth="public", website=True)
    def customer_form_submit(self, **post):
        request.env['repair.order'].create({
            'vin': post.get('vin'),
            'description': post.get('description'),
        })
        return request.render("portal.portal_my_home")