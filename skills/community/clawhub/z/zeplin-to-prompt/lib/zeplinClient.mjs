import { ZeplinApi, Configuration } from "@zeplin/sdk";

export const createZeplinClient = (accessToken) => new ZeplinApi(new Configuration({ accessToken }));

export const fetchLatestScreenVersion = async (api, projectId, screenId) => {
  const res = await api.screens.getLatestScreenVersion(projectId, screenId);
  return res?.data || res;
};
