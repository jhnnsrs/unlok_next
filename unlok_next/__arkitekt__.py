import json
from arkitekt_next.base_models import Manifest
from unlok_next.unlok import Unlok
from unlok_next.rath import UnlokLinkComposition, UnlokRath
from rath.links.split import SplitLink
from fakts_next.contrib.rath.aiohttp import FaktsAIOHttpLink
from fakts_next.contrib.rath.graphql_ws import FaktsGraphQLWSLink
from herre_next.contrib.rath.auth_link import HerreAuthLink
from graphql import OperationType
from herre_next import Herre
from fakts_next import Fakts

from arkitekt_next.service_registry import Params
from arkitekt_next.base_models import Requirement
import os
from fluss_next.fluss import Fluss
from fluss_next.rath import FlussLinkComposition, FlussRath
from rath.links.split import SplitLink
from fakts_next.contrib.rath.aiohttp import FaktsAIOHttpLink
from fakts_next.contrib.rath.graphql_ws import FaktsGraphQLWSLink
from herre_next.contrib.rath.auth_link import HerreAuthLink
from graphql import OperationType
from herre_next import Herre
from fakts_next import Fakts

from arkitekt_next.base_models import Manifest

from arkitekt_next.service_registry import Params, BaseArkitektService
from arkitekt_next.base_models import Requirement


class ArkitektNextUnlok(Unlok):
    rath: UnlokRath


def build_relative_path(*path: str) -> str:
    return os.path.join(os.path.dirname(__file__), *path)


class LokService(BaseArkitektService):

    def get_service_name(self):
        return "unlok"

    def build_service(
        self, fakts: Fakts, herre: Herre, params: Params, manifest: Manifest
    ):
        return ArkitektNextUnlok(
            rath=UnlokRath(
                link=UnlokLinkComposition(
                    auth=HerreAuthLink(herre=herre),
                    split=SplitLink(
                        left=FaktsAIOHttpLink(
                            fakts_group="lok", fakts=fakts, endpoint_url="FAKE_URL"
                        ),
                        right=FaktsGraphQLWSLink(
                            fakts_group="lok", fakts=fakts, ws_endpoint_url="FAKE_URL"
                        ),
                        split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
                    ),
                )
            )
        )

    def get_requirements(self):
        return [
            Requirement(
                key="unlok",
                service="live.arkitekt.lok",
                description="An instance of ArkitektNext Lok to authenticate the user",
            ),
        ]

    def get_graphql_schema(self):
        schema_graphql_path = build_relative_path("api", "schema.graphql")
        with open(schema_graphql_path) as f:
            return f.read()

    def get_turms_project(self):
        turms_prject = build_relative_path("api", "project.json")
        with open(turms_prject) as f:
            return json.loads(f.read())


def build_services():
    return [LokService()]
