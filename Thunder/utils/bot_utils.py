    except Exception as e:
        logger.error(f"Database error in log_newusr for user {uid}: {e}")


async def gen_links(fwd_msg: Message, shortener: bool = True) -> Dict[str, str]:
    base_url = Var.URL.rstrip("/")
    fid = fwd_msg.id
    m_name_raw = get_fname(fwd_msg)
    m_name = m_name_raw.decode('utf-8', errors='replace') if isinstance(m_name_raw, bytes) else str(m_name_raw)
    m_size_hr = humanbytes(get_fsize(fwd_msg))
    enc_fname = quote(m_name)
    f_hash = get_hash(fwd_msg)
    slink = f"{base_url}/watch/{f_hash}{fid}/{enc_fname}"
    olink = f"{base_url}/dl/{f_hash}{fid}/{enc_fname}"

    if shortener and getattr(Var, "SHORTEN_MEDIA_LINKS", False):
        try:
            s_results = await asyncio.gather(shorten(slink), shorten(olink), return_exceptions=True)
            if not isinstance(s_results[0], Exception):
                slink = s_results[0]
            else:
                logger.warning(f"Failed to shorten stream_link: {s_results[0]}")
            if not isinstance(s_results[1], Exception):
                olink = s_results[1]
            else:
                logger.warning(f"Failed to shorten online_link: {s_results[1]}")
        except Exception as e:
            logger.error(f"Error during link shortening: {e}")

    return {"stream_link": slink, "online_link": olink, "media_name": m_name, "media_size": m_size_hr}


async def gen_dc_txt(usr: User) -> str:
    dc_id_val = usr.dc_id if usr.dc_id is not None else MSG_DC_UNKNOWN
    return MSG_DC_USER_INFO.format(user_name=usr.first_name or 'User', user_id=usr.id, dc_id=dc_id_val)


async def get_user(cli: Client, qry: Any) -> Optional[User]:
    if isinstance(qry, str):
        if qry.startswith('@'):
            return await handle_flood_wait(cli.get_users, qry)
        elif qry.isdigit():
            return await handle_flood_wait(cli.get_users, int(qry))
    elif isinstance(qry, int):
        return await handle_flood_wait(cli.get_users, qry)
    return None


async def is_admin(cli: Client, chat_id_val: int) -> bool:
    member = await handle_flood_wait(cli.get_chat_member, chat_id_val, cli.me.id)
    if member is None:
        return False
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


async def reply(msg: Message, **kwargs):
    return await handle_flood_wait(msg.reply_text, **kwargs, quote=True, link_preview_options=LinkPreviewOptions(is_disabled=True))